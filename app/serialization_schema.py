from app import marshmallow
from app.models import Student


class StudentSchema(marshmallow.ModelSchema):
    class Meta:
        model = Student
