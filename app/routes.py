
from app import app, controller
import json
from app.serialization_schema import *
from flask import jsonify, request, render_template, redirect, flash, url_for
from app.forms import LoginForm
from app.models import *
from app import bcrypt
from flask_login import login_user, current_user, logout_user, login_required


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = Teacher.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)


@app.route('/students')
def get_students():
    students = Student.query.all()
    schema = StudentSchema(many=True)
    output = schema.dump(students)
    return jsonify({'student': output})


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        post_data = request.get_json()
        teacher = Teacher.query.filter_by(login=post_data.get('login')).first()
        if teacher and bcrypt.check_password_hash((teacher.password, post_data.get('password'))):
            response_object = {'status': 'success',
                               'name': teacher.name,
                               'surname': teacher.surname,
                               'group_id': teacher.group_id,
                               'subjects': teacher.subjects
            }
            return response_object
        else:
            response_object = {'status': 'error'}
            return response_object

