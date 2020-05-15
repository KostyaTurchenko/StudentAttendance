from app.models import *


def add_item(data):
    db.session.add(data)
    db.session.commit()


def get_groups(course):
    return Group.query.filter_by(course=course).all()


def get_students_by_group(group_id):
    return Student.query.filter_by(group_id=group_id).all()


def get_subjects():
    return Subject.query.all()


def get_absent_dates(group_id, subject_id):
    return Absent.query.filter_by(group_id=group_id, subject_id=subject_id).all()


def add_absent_date(group_id, subject_id, student_id, date):
    new_a = Absent(group_id=group_id, subject_id=subject_id, student_id=student_id, date=date)
    add_item(new_a)
    return new_a


def delete_absent_date(id):
    Absent.query.filter_by(id=id).delete()
    db.session.commit()


def add_student(first_name, last_name):
    new_stud = Student(firtsname=first_name, lastname=last_name)
    add_item(new_stud)


