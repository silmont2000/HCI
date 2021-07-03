import os
from sys import prefix

from flask import Flask


__all__ = ['Config']

from app import app


class Config(object):
    """配置参数"""
    # sqlalchemy的配置参数，sqlite:///db.sqlite3表示使用本地文件
    SQLALCHEMY_DATABASE_URI = "sqlite:///auth.sqlite3"
    # 连接数据库 type=mysql   user:password  localhost
    # SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/auth"
    # 设置成 True，SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CSRF_ENABLED = True
    # Socketio用
    SECRET_KEY = os.getenv('SECRET_KEY', '3180102829')

