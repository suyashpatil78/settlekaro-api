import marshmallow as ma
from marshmallow import Schema

class UsersSchema(Schema):
    id = ma.fields.String(allow_none=False)
    email = ma.fields.String(allow_none=False)
    username = ma.fields.String(allow_none=False)
