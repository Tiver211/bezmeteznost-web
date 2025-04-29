from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    login = fields.String(required=True)
    mail = fields.Email(required=True)
    password = fields.String(required=True)

