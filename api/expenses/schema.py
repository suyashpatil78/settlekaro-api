import marshmallow as ma
from marshmallow import Schema

class ExpensesSchema(Schema):
    id = ma.fields.String(allow_none=False)
    created_by = ma.fields.String(allow_none=False)
    date = ma.fields.Date(allow_none=False)
    amount = ma.fields.Float(allow_nan=False)
    expense_details = ma.fields.List(allow_none=False)