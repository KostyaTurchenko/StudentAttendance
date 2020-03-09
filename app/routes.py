
from app import app, controller
import json
from functools import wraps
from app.serialization_schema import *
from flask import jsonify, request, render_template, redirect, flash, url_for
from app.forms import LoginForm
from app.models import *
from app import bcrypt
from datetime import datetime, timedelta
import jwt
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

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = Teacher.query.filter_by(login=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@app.route('/students')
@token_required
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
            token = jwt.encode({
                'sub': teacher.login,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=30)},
                app.config['SECRET_KEY'])
            response_object = {'status': 'success',
                               'token': token.decode('utf-8'),
                               'name': teacher.name,
                               'surname': teacher.surname,
                               'group_id': teacher.group_id,
                               'subjects': teacher.subjects
            }
            return response_object
        else:
            response_object = {'status': 'error'}
            return jsonify(response_object)

