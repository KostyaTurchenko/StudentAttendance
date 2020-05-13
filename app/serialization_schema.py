from app import marshmallow
from app.models import Student, Group, Subject, Absent


class StudentSchema(marshmallow.ModelSchema):
    class Meta:
        model = Student


class GroupSchema(marshmallow.ModelSchema):
    class Meta:
        model = Group


class SubjectSchema(marshmallow.ModelSchema):
    class Meta:
        model = Subject


class AbsentSchema(marshmallow.ModelSchema):
    class Meta:
        model = Absent
        include_fk = True
