from flask import Flask, jsonify
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

from flask_bcrypt import Bcrypt

from flask_login import LoginManager

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'topsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base_dir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

CORS(app)

from app import routes, models

admin = Admin(app, 'App', url='/', index_view=AdminIndexView(name='home'))
admin.add_view(ModelView(models.Student, db.session))
admin.add_view(ModelView(models.Group, db.session))