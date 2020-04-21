
from app import app, controller
import json
from functools import wraps
from app.serialization_schema import *
from flask import jsonify, request, render_template, redirect, flash, url_for, send_from_directory
from app.forms import LoginForm
from app.models import *
from app import bcrypt
from datetime import datetime, timedelta
import jwt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, date, time


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
        print(len(auth_headers))
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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/static/<path:path>')
def static_dist(path):
    # тут пробрасываем статику
    return send_from_directory("/dist", path)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        post_data = request.get_json()
        teacher = Teacher.query.filter_by(login=post_data.get('login')).first()
        if teacher and bcrypt.check_password_hash(teacher.password, post_data.get('password')):
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

# TODO: Возвращать структуру как response_object
@app.route('/courses')
@token_required
def get_courses(user):
    response_object = {
        'courses': [
            {
                'id': 321,
                'order': 1,
                'groups': [
                    {
                        'id': 323,
                        'name': '1.2F',
                        'subjects': [
                            {
                                'id': 12,
                                'name': 'OC'
                            },
                            {
                                'id': 13,
                                'name': 'IT'
                            }
                        ]
                    },
                    {
                        'id': 324,
                        'name': '1.1F',
                        'subjects': [
                            {
                                'id': 12,
                                'name': 'OC'
                            },
                            {
                                'id': 14,
                                'name': 'TI'
                            }
                        ]
                    }
                ]
            },
            {
                'id': 322,
                'order': 2,
                'groups': [
                    {
                        'id': 325,
                        'name': '1.1E',
                        'subjects': [
                            {
                                'id': 16,
                                'name': 'Информатика'
                            },
                            {
                                'id': 13,
                                'name': 'IT'
                            }
                        ]
                    }
                ]
            }
        ]
    }

    return jsonify(response_object)

#Для дебага (потом удалить)
students_list = [
    {
        'id': 2134,
        'name': "Alex Red",
        'dates': [
            datetime.strptime('09-04-2020', '%d-%m-%Y'),
            datetime.strptime('10-04-2020', '%d-%m-%Y'),
            datetime.strptime('11-04-2020', '%d-%m-%Y')
        ]
    },
    {
        'id': 2234,
        'name': "Dominic Raider",
        'dates': [

        ]
    },
    {
        'id': 2243,
        'name': "John Lenon",
        'dates': [

        ],
    }
]

# TODO: Возвращать список студентов в соответствии запросу
@app.route("/students", methods=['POST'])
@token_required
def get_students(user):
    post_data = request.get_json()
    print(post_data.get('course').get('id'))
    # post_data.course.id - id курса
    # post_data.group.id - id группы
    # post_data.subject.id - id предмета

    #students = Student.query.all()
    #schema = StudentSchema(many=True)
    #output = schema.dump(students)
    response_object = {
        'students': students_list
    }
    return jsonify(response_object)


# TODO: добавление пропуска (Если у каждого дня есть свой id, то следует отпралять этот ид)
@app.route("/absenteeism/add", methods=['POST'])
@token_required
def add_absenteeism(user):
    post_data = request.get_json()

    stud_id = post_data.get('studentId')
    date = post_data.get('date')
    pDate = datetime.strptime(date, '%d-%m-%Y')

    print(date)
    print(pDate)
    #Приходит объект с ид студента, датой, предметом
    #Если всё хорошо, возвращаем True
    return jsonify({ 'status': True, 'date': pDate })

# TODO: удаление пропуска
@app.route("/absenteeism/remove", methods=['POST'])
@token_required
def remove_absenteeism(user):
    post_data = request.get_json()

    stud_id = post_data.get('studentId')
    date = post_data.get('date')
    pDate = datetime.strptime(date, '%d-%m-%Y')

    print(pDate)
    #Приходит объект с ид студента, датой, предметом
    #Если всё хорошо, возвращаем True
    return jsonify({ 'status': True })
