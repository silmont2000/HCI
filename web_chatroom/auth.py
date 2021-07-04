from flask import Blueprint, jsonify, url_for
from flask import render_template
from flask import request
from flask_login import login_required, logout_user, login_user
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from . import db, login_manager
from .models import User, init_db, init_msg
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField(
        'repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register')

    def validate_username(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError('换个名字吧！')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')

    def validate_username(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user is None:
            raise ValidationError('您还没有注册！')


auth = Blueprint('auth', __name__)


# 初始化用
@auth.route('/db', methods=['GET', 'POST'])
def create_db():
    init_db()
    return "OK"


# 初始化用
@auth.route('/msg', methods=['GET', 'POST'])
def create_msgdb():
    init_msg()
    return "OK"


@auth.route('/login', methods=['GET', "POST"], endpoint='login')
def login():
    login_form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=login_form)
    elif login_form.validate():
        name = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(name=name).first()
        if user.verify_password(password=password):
            login_user(user)
            return redirect(url_for("chat.chatroom"))
        else:
            login_form.password.errors.append('密码错误！')
    return render_template('/login.html', form=login_form)


@auth.route('/register', methods=['GET', "POST"], endpoint='register')
def register():
    register_form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', form=register_form)
    elif register_form.validate():
        name = register_form.username.data
        password = register_form.password.data
        db.session.add(User(name, password))
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        return render_template('register.html', form=register_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()  # 登出用户
    return render_template('/index.html')


# Flask-Login 提供了一个 current_user 变量，注册这个函数的目的是，当程序运行后，如果用户已登录， current_user 变量的值会是当前用户的用户模型类记录。
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象
