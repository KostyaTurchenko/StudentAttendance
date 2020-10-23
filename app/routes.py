from app import app, controller
from functools import wraps
from app.serialization_schema import *
from flask import jsonify, request, render_template, send_from_directory
from app.models import *
from app import bcrypt
from datetime import timedelta
import jwt
from datetime import datetime


# http://kirillchernyshov.pythonanywhere.com/


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


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        post_data = request.get_json()
        if not Teacher.query.filter_by(login=post_data.get('login')).first():
            salt = bcrypt.gensalt()
            password = post_data.get('password')
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            controller.add_teacher(post_data.get('name'),
                                   post_data.get('surname'),
                                   post_data.get('login'),
                                   hashed_password)
            response_object = {'status': True}
            return jsonify(response_object)
        else:
            response_object = {'status': 'already exist'}
            return jsonify(response_object)




@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        post_data = request.get_json()
        teacher = Teacher.query.filter_by(login=post_data.get('login')).first()
        # if teacher and bcrypt.check_password_hash(teacher.password, post_data.get('password')):
        print(post_data.get('password'))
        print(teacher.password)
        if teacher and bcrypt.checkpw(post_data.get('password').encode('utf-8'), teacher.password):
            token = jwt.encode({
                'sub': teacher.login,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=30)},
                app.config['SECRET_KEY'])
            response_object = {'status': 'success',
                               'token': token.decode('utf-8'),
                               'name': teacher.name,
                               'surname': teacher.surname,
            }
            return jsonify(response_object)
        else:
            response_object = {'status': 'error'}
            return jsonify(response_object)

# salt = bcrypt.gensalt()
# hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
# user = User(username=username, email=email, password=hashed_password)


# приходит json в таком виде: { 'course': 1 }
@app.route("/groups", methods=['POST'])
@token_required
def get_groups(user):
    post_data = request.get_json()
    groups = controller.get_groups(post_data['course'])
    schema = GroupSchema(many=True)
    view_groups = schema.dump(groups)
    response_object = {
        'groups': view_groups
    }
    return jsonify(response_object)


# TODO: Возвращать список студентов в соответствии запросу
# приходит json в таком виде: { 'group_id': 1 }
@app.route("/students", methods=['POST'])
@token_required
def get_students(user):
    post_data = request.get_json()
    #print(post_data.get('course').get('id'))
    # post_data.course.id - id курса
    # post_data.group.id - id группы
    # post_data.subject.id - id предмета

    # json групп на входе будет отличаться от того что выше(курс -
    # это поле объекта group
    students = controller.get_students_by_group(post_data['group_id']) # 1 - Это для дебуга
    schema = StudentSchema(many=True)
    view_students = schema.dump(students)
    response_object = {
        'students': view_students
    }
    return jsonify(response_object)


@app.route("/subjects", methods=['GET'])
@token_required
def get_subjects(user):
    subjects = controller.get_subjects()
    schema = SubjectSchema(many=True)
    view_subjects = schema.dump(subjects)
    response_object = {
        'subjects': view_subjects
    }
    return jsonify(response_object)


@app.route("/absenteeism/all", methods=['POST'])
@token_required
def get_absenteeism_for_group(user):
    post_data = request.get_json()

    subject_id = post_data['subjectId']
    group_id = post_data['groupId']

    dates = controller.get_absent_dates(group_id, subject_id)
    schema = AbsentSchema(many=True)
    view_dates = schema.dump(dates)
    response_object = {
        'dates': view_dates
    }
    return jsonify(response_object)


# TODO: добавление пропуска (Если у каждого дня есть свой id, то следует отпралять этот ид)
@app.route("/absenteeism/add", methods=['POST'])
@token_required
def add_absenteeism(user):
    post_data = request.get_json()

    subject_id = post_data['subjectId']
    group_id = post_data['groupId']
    stud_id = post_data['studentId']
    date = post_data['date']
    p_date = datetime.strptime(date, '%d-%m-%Y')

    d = controller.add_absent_date(group_id, subject_id, stud_id, p_date)

    schema = AbsentSchema(many=False)
    view_absent = schema.dump(d)

    response_object = {
        'status': True,
        'date': view_absent

    }
    return jsonify(response_object)


# TODO: удаление пропуска
@app.route("/absenteeism/remove", methods=['POST'])
@token_required
def remove_absenteeism(user):
    post_data = request.get_json()

    absent_id = post_data['absentId']
    controller.delete_absent_date(absent_id)

    return jsonify({'status': True})
