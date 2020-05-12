from app import marshmallow
from app.models import Student, Group


class StudentSchema(marshmallow.ModelSchema):
    class Meta:
        model = Student


class GroupSchema(marshmallow.ModelSchema):
    class Meta:
        model = Group
