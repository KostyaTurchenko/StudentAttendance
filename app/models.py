from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Teacher.query.get(int(user_id))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return "<student {} {}>".format(self.name, self.surname)


class Teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    login = db.Column(db.String(64))
    password = db.Column(db.String(256))


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return "student {} {}".format(self.name)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Float)
    course = db.Column(db.Integer)
    students = db.relationship('Student', backref='group', lazy=True)

    def __repr__(self):
        return "<course {} group {}".format(self.course, self.number)


class Absent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    date = db.Column(db.Date)
