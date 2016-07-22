# coding:utf-8
from flask import Blueprint, render_template, flash,redirect, url_for, request,session
from flask_login import login_required, login_user, LoginManager
from indoorlocation.forms import *
from indoorlocation.models import *

main = Blueprint('main', __name__)
login_manager = LoginManager()

# 用户登录接口
@main.route('/', methods=['GET', 'POST'], endpoint='login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.home'))
        else:
            flash(u'无效的用户名或密码。')
    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/home', endpoint='home')
@login_required
def home():
    return render_template('home.html')