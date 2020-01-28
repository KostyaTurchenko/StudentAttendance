from app.models import *
from calendar import *


def _add_in_table(item):
    db.session.add(item)
    db.session.commit()


def add_student(name, surname, group_id):
    stud = Student(name=name, surname=surname, group_id=group_id)
    _add_in_table(stud)


def add_group(number, course):
    group = Group(number=number, course=course)
    _add_in_table(group)


def add_subject(name):
    subj = Subject(name=name)
    _add_in_table(subj)


def get_students_for_group(course, group_number):
    group = Group.query.filter_by(course=course, number=group_number).first()
    return group.students


def set_schedule(start_day, end_day):
    pass

