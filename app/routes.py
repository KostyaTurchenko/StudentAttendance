from app import app
from app import app, controller
from flask import request, render_template, redirect, flash, url_for
from app.forms import LoginForm
from app.models import *
from app import bcrypt
from flask_security import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/main.html')
def main_page():
    return "Hi my freands!"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Teacher.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)