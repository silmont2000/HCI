from flask import Blueprint, jsonify, url_for
from flask import render_template
from flask import request
from flask_login import login_required, logout_user, login_user
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from . import db, login_manager
from .models import User, init_db
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')


auth = Blueprint('auth', __name__)


# 初始化用
@auth.route('/db', methods=['GET', 'POST'])
def create_db():
    init_db()
    return "OK"


@auth.route('/login', methods=['GET', "POST"], endpoint='login')
def login():
    login_form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=login_form, info='0')
    elif request.method == 'POST':
        if login_form.validate_on_submit():
            name = login_form.username.data
            password = login_form.password.data
            user = User.query.filter_by(name=name).first()
            if user.verify_password(password=password):
                login_user(user)
                return redirect(url_for("chat.chatroom"))
            else:
                return render_template('/login.html', form=login_form, info=name)


@auth.route('/register', methods=['GET', "POST"], endpoint='register')
def register():
    register_form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', form=register_form)
    else:
        name = register_form.username.data
        password = register_form.password.data
        db.session.add(User(name, password))
        db.session.commit()
        return redirect(url_for('auth.login'))


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
