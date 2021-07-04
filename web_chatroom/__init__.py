import logging

import redis
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# 控制訪問
__all__ = ['db', 'login_manager', 'bootstrap', 'r', 'create_app', ]

db = SQLAlchemy()
login_manager = LoginManager()  # 实例化登录管理对象
bootstrap = Bootstrap()
r = redis.Redis(
    host='redis-19668.c1.us-west-2-2.ec2.cloud.redislabs.com',
    port=19668,
    password='baiyudi66',
    decode_responses=True)


def create_app():
    app = Flask(__name__)
    app.debug = True
    # 必須先配置再綁定db和app
    app.config.from_object(Config)

    # 延迟初始化
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint 验证失败时要跳转的页面

    app.logger.setLevel(logging.DEBUG)
    from web_chatroom.auth import auth
    app.register_blueprint(auth)
    from web_chatroom.chat import chat
    app.register_blueprint(chat)
    from web_chatroom.capture import capture
    app.register_blueprint(capture)

    return app
