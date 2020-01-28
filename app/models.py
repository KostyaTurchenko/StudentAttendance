
from app import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    absence_dates = db.relationship('Schedule', secondary='absent', backref='absent_students', lazy=True)

    def __repr__(self):
        return "<student {} {}".format(self.name, self.surname)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    login = db.Column(db.String(64))
    password = db.Column(db.String(256))
    group_id = db.Column(db.Integer)
    subjects = db.relationship('Subject', secondary='teacher_subject', backref='teachers', lazy=True)


class TeacherSubject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    groups = db.relationship('Group', secondary='teacher_subject_group', backref='teachers_subjects', lazy=True)


class TeacherSubjectGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    teacher_subject_id = db.Column(db.Integer, db.ForeignKey('teacher_subject.id'))


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Float)
    course = db.Column(db.Integer)
    students = db.relationship('Student', backref='group', lazy=True)
    schedule = db.relationship('Schedule', secondary='group_schedule', backref='groups', lazy=True)

    def __repr__(self):
        return "<course {} group {}".format(self.course, self.number)


class GroupSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    day_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)


class Absent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    day_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))