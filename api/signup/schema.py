import marshmallow as ma
from marshmallow import Schema

class SignupSchema(Schema):
    email = ma.fields.String(allow_none=False)
    password = ma.fields.String(load_only=True, allow_none=False)
    username = ma.fields.String(allow_none=False)
