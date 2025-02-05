from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    student_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    student_id = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    student_course = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    
    class Meta:
        strict = True