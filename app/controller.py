from app.models import *
import calendar


def db_commit(data):
    db.session.add(data)
    db.session.commit()


def get_students():
    return Student.query.all()


def get_groups(course):
    return Group.query.filter_by(course=course).all()


def get_students_by_group(group_id):
    return Student.query.filter_by(group_id=group_id).all()


def add_student(first_name, last_name):
    new_stud = Student(firtsname=first_name, lastname=last_name)
    new_stud.bd_commit(new_stud)

