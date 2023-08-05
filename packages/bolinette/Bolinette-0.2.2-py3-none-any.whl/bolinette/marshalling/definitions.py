from bolinette import response, marshalling
from bolinette.exceptions import EntityNotFoundError

_registered_models = {}
_registered_responses = {}
_registered_payloads = {}


def _get_def(collection, key):
    d = collection.get(key)
    if d is None:
        response.abort(*response.internal_server_error(f'marshalling.unknown_definition:{key}'))
    return d


def get_response(key):
    return _get_def(_registered_responses, key)


def get_payload(key):
    return _get_def(_registered_payloads, key)


def get_model(name):
    return _registered_models.get(name)


def register(model, name):
    def create_defs(collection, params):
        for param in params:
            if isinstance(param, list):
                key = 'default'
                payload = param
            else:
                key, payload = param
            definition = marshalling.Definition(name, name, key)
            for field in payload:
                definition.fields.append(field)
            collection[definition.key] = definition
    if hasattr(model, 'payloads'):
        create_defs(_registered_payloads, model.payloads())
    if hasattr(model, 'responses'):
        create_defs(_registered_responses, model.responses())
    if name not in _registered_models:
        _registered_models[name] = model


def marshall(definition, entity, skip_none=False, as_list=False):
    if as_list:
        return [marshall(definition, e, skip_none, False) for e in entity]
    data = {}
    for field in definition.fields:
        if isinstance(field, marshalling.Field):
            if field.function is not None:
                value = field.function(entity)
            else:
                value = getattr(entity, field.name, None)
            if field.formatting is not None:
                value = field.formatting(value)
            if not skip_none or value is not None:
                data[field.name] = value
        elif isinstance(field, marshalling.Definition):
            d = get_response(field.key)
            data[field.name] = marshall(d, getattr(entity, field.name), skip_none, False)
        elif isinstance(field, marshalling.List):
            d = get_response(field.element.key)
            data[field.name] = marshall(d, getattr(entity, field.name), skip_none, True)
    return data


def link_foreign_entities(definition, params):
    errors = []
    for field in definition.fields:
        if isinstance(field.type, marshalling.types.classes.ForeignKey):
            value = params.get(field.name, None)
            model = get_model(field.type.model)
            if value is not None and model is not None:
                entity = model.query.filter_by(**{field.type.key: value}).first()
                if entity is None:
                    errors.append((field.type.model, field.type.key, value))
    if len(errors) > 0:
        raise EntityNotFoundError(params=errors)
