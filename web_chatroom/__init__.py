import os
from sys import prefix

from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# 控制訪問
__all__ = ['db', 'login_manager']

db = SQLAlchemy()
login_manager = LoginManager()  # 实例化登录管理对象


def create_app():
    app = Flask(__name__)
    app.debug = True
    # 必須先配置再綁定db和app
    app.config.from_object(Config)
    # 延迟初始化
    db.init_app(app)
    login_manager.init_app(app)  # 初始化应用
    login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint 验证失败时要跳转的页面
    from web_chatroom.auth import auth
    app.register_blueprint(auth)
    from web_chatroom.chat import chat
    app.register_blueprint(chat)

    return app
