from app.models import *
import calendar


@staticmethod
def db_commit(data):
    db.session.add(data)
    db.session.commit()


@staticmethod
def get_students():
    return Student.query.all()


@staticmethod
def add_student(first_name, last_name):
    new_stud = Student(firtsname=first_name, lastname=last_name)
    new_stud.bd_commit(new_stud)

