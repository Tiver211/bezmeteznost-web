from .auth import *

def validate_schema(schema: Schema, **kwargs):
    try:
        schema = schema()
        schema.load(data=kwargs)
        return True
    except ValidationError as err:
        return False
