
import weakref
from collections import defaultdict as dd
from contextlib import suppress
from functools import lru_cache

import sqlalchemy as sql
import orjson
from aiohttp import web
from aiohttp.hdrs import METH_ALL

from marshmallow import (
    fields,
    missing,
    post_load,
    validate,
    validates
)
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import DDL

from . import (
    hooks,
    fields as postschema_fields,
    validators as postschema_validators
)
from .auth.perms import TopSchemaPermFactory, AuxSchemaPermFactory
from .schema import DefaultMetaBase
from .spec import APISpecBuilder
from .utils import retype_schema
from .view import AuxViewBase, ViewsBase, ViewsTemplate

Base = declarative_base()

METH_ALL = [meth.lower() for meth in METH_ALL]
ITERABLE_FIELDS = (
    fields.List,
    postschema_fields.Set
)


def popattr(cls, attr):
    with suppress(AttributeError):
        delattr(cls, attr)


def getattrs(cls):
    return {k: v for k, v in cls.__dict__.items() if not k.startswith('__')}


def create_model(schema_cls, info_logger): # noqa
    name = schema_cls.__name__
    methods = dict(schema_cls.__dict__)
    try:
        tablename = methods.get('__tablename__', getattr(schema_cls, '__tablename__'))
        model_methods = {
            '__tablename__': tablename
        }
    except KeyError:
        raise AttributeError(f'{name} needs to define `__tablename__`')

    meta = methods.get('Meta')
    declared_fields = methods['_declared_fields']

    if hasattr(meta, '__table_args__'):
        model_methods['__table_args__'] = meta.__table_args__

    for fieldname, field_attrs in declared_fields.items():
        if isinstance(field_attrs, fields.Field):
            if isinstance(field_attrs, postschema_fields.AutoSessionField):
                perms = getattr(methods.get('Public'), 'permissions', None)
                if perms and hasattr(perms, 'post') and 'primary_key' in field_attrs.metadata:
                    # auto-injected primary key is based on the session context, 
                    # so we can't allow public posts.
                    raise AttributeError(f"{name} can't include 'post' as a public permission attribute")

            metadata = field_attrs.metadata
            try:
                field_instance = metadata.pop('sqlfield', None) or metadata['fk']
                if not field_instance:
                    continue
            except KeyError:
                # skip fields with no sql bindings
                continue
            except AttributeError:
                raise AttributeError(
                    f'Schema field `{fieldname}` needs to define a SQLAlchemy field instance')

            translated = {}
            default_value = field_attrs.default
            if default_value != missing:
                translated['server_default'] = default_value

            args = []
            if 'fk' in metadata:
                args.append(metadata['fk'])
            if 'autoincrement' in metadata:
                args.append(metadata.pop('autoincrement'))
            metadict = metadata.copy()
            metadict.pop('fk', None)
            metadict.pop('read_only', None)

            model_methods[fieldname] = sql.Column(field_instance, *args, **metadict, **translated)

    modelname = name + 'Model'
    new_model = type(modelname, (Base,), model_methods)

    model_events = methods.get('Events')
    if model_events is not None:
        for k, v in model_events.__dict__.items():
            if not k.startswith('__'):
                event.listen(new_model.__table__, k, DDL(v))

    info_logger.debug(f"- created model `{modelname}`")
    return new_model


class ViewMaker:
    def __init__(self, schema_cls, router, registered_schemas, url_prefix):
        self.url_prefix = url_prefix
        self.schema_cls = schema_cls
        self.router = router
        self.registered_schemas = registered_schemas
        meta_cls = self.rebase_metaclass()
        self.schema_cls.Meta = meta_cls
        self.meta_cls = meta_cls

    @property
    def excluded_ops(self):
        return self.meta_cls.excluded_ops

    @property
    @lru_cache()
    def base_resource_url(self):
        route_base = self.meta_cls.route_base.replace('/', '').lower()
        return f'{self.url_prefix}/{route_base}/'

    def create_views(self, joins):
        # common definitions
        schema_name = self.schema_cls.__name__.title()
        view_methods = {}
        base_methods = {}
        model = self.schema_cls._model

        base_methods['model'] = model
        base_methods['schema_cls'] = self.schema_cls
        base_methods['tablename'] = model.__tablename__
        view_methods.update(base_methods)

        # only use these methods off the ViewsTemplate that make sense for our use case
        for method_name, method in ViewsTemplate.__dict__.items():
            if not method_name.startswith('__'):
                if method_name in self.excluded_ops:
                    continue
                view_methods[method_name] = method

        # create the web.View-derived view
        cls_view = type(f'{schema_name}View', (ViewsBase,), view_methods)
        cls_view.registered_schemas = weakref.proxy(self.registered_schemas)
        cls_view.post_init(joins)

        self.router.add_route("*", self.base_resource_url, cls_view)

        return cls_view

    def create_aux_views(self, parent_cls_view, perm_builder):
        def gen():
            yield
        all_ops = ['post', 'get', 'patch', 'put', 'delete', 'list']

        class mod_parent_base(parent_cls_view):
            pass

        if hasattr(self.schema_cls, '__aux_routes__'):
            for routename, proto_viewcls in self.schema_cls.__aux_routes__.items():
                if routename.startswith('/'):
                    routename = routename[1:]
                if not routename.endswith('/'):
                    routename += '/'
                url = self.base_resource_url + routename
                view_methods = dict(proto_viewcls.__dict__)

                # ensure _iter is inherited from AuxViewBase, not ViewsClassBase
                view_methods['_iter'] = AuxViewBase._iter
                view_cls = type(
                    proto_viewcls.__qualname__,
                    (mod_parent_base, AuxViewBase),
                    view_methods)

                perms = perm_builder(proto_viewcls)
                view_cls._perm_options = {
                    'perms': perms,
                    **perm_builder.operation_constraints
                }
                # view_cls._disallow_authed = perm_builder.disallow_authed

                allowed = [op for op in all_ops if op in view_methods]
                for op in all_ops:
                    if hasattr(view_cls, op) and op not in view_methods:
                        setattr(view_cls, op, lambda self: gen().throw(
                            web.HTTPMethodNotAllowed(method=op, allowed_methods=allowed))
                        )
                self.router.add_route("*", url, view_cls)
                yield routename, view_cls

    @property
    def omit_me(self):
        return not self.meta_cls.create_views

    def make_new_post_view(self, schema_cls):
        return self.__class__.__base__(schema_cls, self.router)

    def rebase_metaclass(self):
        meta_cls = self.schema_cls.Meta
        meta_methods = dict(meta_cls.__dict__)

        # force-set common meta attrs
        meta_methods.setdefault('route_base', self.schema_cls.__name__.lower())
        meta_methods['render_module'] = orjson

        new_meta = type('Meta', (DefaultMetaBase, ), meta_methods)
        self.schema_cls.Meta = new_meta
        return new_meta

    def process_relationships(self):
        joins = {}

        new_schema_methods = {}
        self.schema_cls._m2m_where_stmts = relation_where_stmts = {}
        this_table, this_pk = str(
            self.schema_cls._model.__table__.primary_key.columns_autoinc_first[0]).split('.')

        deletion_cascade = getattr(self.schema_cls, '_deletion_cascade', [])
        m2m_cherrypicks = getattr(self.schema_cls, '_m2m_cherrypicks', [])

        for fieldname, fieldval in self.schema_cls._declared_fields.items():
            if isinstance(fieldval, postschema_fields.Relationship):
                if isinstance(fieldval, postschema_fields.AutoSessionField) and 'primary_key' in fieldval.metadata:
                    # omit session-based auto-injected pks
                    continue
                this_target = (fieldname, this_table, this_pk)
                foreign_target = fieldval.target_table
                linked_table = foreign_target['name']
                linked_table_pk = foreign_target['pk']
                linked_target = (linked_table_pk, linked_table, fieldname)
                linked_schema = self.registered_schemas @ linked_table
                linked_schema.pk_column_name = linked_table_pk
                linked_schema._deletion_cascade = getattr(linked_schema, '_deletion_cascade', [])
                linked_schema._m2m_cherrypicks = getattr(linked_schema, '_m2m_cherrypicks', [])

                if isinstance(fieldval, postschema_fields.AutoSessionForeignResource):
                    validator_fn = postschema_validators.autosession_field_validator(fieldname)
                    new_schema_methods[f'validate_{fieldname}'] = validates(fieldname)(validator_fn)

                elif isinstance(fieldval, postschema_fields.ForeignResources):
                    # in the deletes departments, we need to faciliate the following scenario:
                    # - one of our parent's ForeignResources' fks gets deleted
                    # - its FK reference in our parent needs to be cleared too
                    linked_schema._m2m_cherrypicks.append((this_table, fieldname, this_pk))

                    # The holder of this field will store references to its 'relatives'
                    # Hook a custom validator to ensure that incoming FKs correspond to valid records
                    children_validator, make_children_post_load = \
                        postschema_validators.adjust_children_field(fieldname)

                    # add the validator only in case of this schema being used for writing
                    new_schema_methods[f'validate_{fieldname}'] = validates(fieldname)(children_validator)

                    # ensure that ForeignResources' value is formatted correctly
                    new_schema_methods[f'post_load_{fieldname}'] = post_load(make_children_post_load)
                    relation_where_stmts[fieldname] = f'{fieldname} ?& %({fieldname})s'

                elif isinstance(fieldval, postschema_fields.ForeignResource):
                    if not fieldval.metadata.get('unique', False):
                        linked_schema._deletion_cascade.append(this_target)
                    else:
                        # unique clause in, t's a O2O relationship,
                        # delete instruction should be present on both tables
                        deletion_cascade.append(linked_target)
                        linked_schema._deletion_cascade.append(this_target)  # this is debatable

                    joins[fieldname] = [linked_schema, f'{linked_table}.{{subkey}}=%({{fill}})s']

        new_schema_methods['_deletion_cascade'] = deletion_cascade
        new_schema_methods['_m2m_cherrypicks'] = m2m_cherrypicks
        self.schema_cls = retype_schema(self.schema_cls, new_schema_methods)
        return joins


def adjust_fields(schema_cls):
    declared_fields = dict(schema_cls._declared_fields)
    iterables = []
    rangeables = []
    for coln, colv in declared_fields.items():
        meta = colv.metadata
        if not colv.required or meta.get('primary_key', False):
            colv.metadata['nullable'] = True
        else:
            colv.metadata['nullable'] = False
        # if the field is a String, then take the max len and use it
        # to create a marshmallow validator
        if isinstance(colv, fields.String):
            sqlfield = colv.metadata.get('sqlfield')
            if sqlfield is not None:
                with suppress(AttributeError):
                    # sqlalchemy field in use could be inheriting from `String` class
                    validator = validate.Length(max=sqlfield.length)
                    colv.validators.append(validator)
        elif isinstance(colv, postschema_fields.RangeField):
            rangeables.append(coln)
        elif isinstance(colv, ITERABLE_FIELDS):
            # ensure relation fields are not included
            if not isinstance(colv, postschema_fields.Relationship):
                iterables.append(coln)

    schema_meta = schema_cls.Meta
    omit_me = not getattr(schema_meta, 'create_views', True)
    if not omit_me:
        pv_hooks = []
        if rangeables:
            pv_hooks.append(hooks.escape_rangeable(rangeables))
        if iterables:
            pv_hooks.append(hooks.escape_iterable(iterables))
        schema_cls._post_validation_write_cleaners.extend(pv_hooks)
    return schema_cls


def build_app(app, registered_schemas):
    app.info_logger.debug("* Building views...")
    router = app.router

    created = dd(int)

    for schema_name, schema_cls in registered_schemas:
        tablename = getattr(schema_cls, '__tablename__', None)
        app.info_logger.debug(f'+ processing {tablename}')

        schema_cls._post_validation_write_cleaners = []
        adjust_fields(schema_cls)

        # create an SQLAlchemy model
        if tablename is not None:
            schema_cls._model = create_model(schema_cls, app.info_logger)
            created['Models'] += 1

    perm_builder = TopSchemaPermFactory(registered_schemas, app.config.roles)
    aux_perm_builder = AuxSchemaPermFactory(registered_schemas, app.config.roles)

    spec_builder = APISpecBuilder(app, router)

    for schema_name, schema_cls in registered_schemas:
        post_view = ViewMaker(schema_cls, router, registered_schemas, app.url_prefix)
        # invoke the relationship processing
        joins = post_view.process_relationships()

        # skip the routes creation, should it be demanded
        if post_view.omit_me:
            continue

        perms = perm_builder(schema_cls)
        cls_view = post_view.create_views(joins)
        cls_view._perm_options = {
            'perms': perms,
            **perm_builder.operation_constraints
        }
        created['Views'] += 1
        aux_routes = dict(post_view.create_aux_views(cls_view, aux_perm_builder))
        if aux_routes:
            schema_cls.__aux_routes__ = aux_routes
            setattr(registered_schemas, schema_name, schema_cls)

        created['Auxiliary views'] += len(aux_routes)
        spec_builder.add_schema_spec(schema_cls, post_view, cls_view, aux_routes.values())

    app.info_logger.info('System ready', created=dict(created))
    return router, spec_builder.build_spec()
