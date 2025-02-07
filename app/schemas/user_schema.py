from marshmallow import Schema, fields, validate
from pydantic import BaseModel, Field


# Validate with Marshmallow
class UserCreateSchema(Schema):
    student_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    student_id = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    student_course = fields.Str(required=True, validate=validate.Length(min=1, max=100))

    class Meta:
        strict = True

# Validate with Pydantic
class UserCreate(BaseModel):
    student_name: str = Field(..., min_length=1, max_length=100)
    student_id: str = Field(..., min_length=1, max_length=50)
    student_course: str = Field(..., min_length=1, max_length=100)
