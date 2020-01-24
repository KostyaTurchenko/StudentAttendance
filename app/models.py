
from app import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    absence_dates = db.relationship('Absent', lazy=True)

    def __repr__(self):
        return "<student {} {}".format(self.name, self.surname)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    absence_students = db.relationship('Absent', lazy=True)


class Absent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    day_id = db.Column(db.DateTime, db.ForeignKey('schedule.id'))
    group_id = db.Column(db.String, db.ForeignKey('group.id'))