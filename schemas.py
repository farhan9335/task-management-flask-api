from marshmallow import Schema,fields
from marshmallow.validate import OneOf,Length

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True,validate=Length(min=3))
    description = fields.Str()
    status = fields.Str(required=True,validate=OneOf(["OPEN","IN_PROGRESS","COMPLETED"]))
    due_date = fields.DateTime(required=True)
    assigned_to = fields.Str(required=True)

class TaskUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    status = fields.Str(validate=OneOf(["OPEN","IN_PROGRESS","COMPLETED"]))
    due_date = fields.DateTime()
    assigned_to = fields.Str()

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Str()

class UpdateUserSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

