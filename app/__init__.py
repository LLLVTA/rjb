# coding:   utf-8
# 作者(@Author):   Messimeimei
# 创建时间(@Created_time): 2023/1/3 1:54

# """构建app，注册蓝图"""

from flask import Flask
from app.config import BaseConfig
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
db = SQLAlchemy()


def register_bp(app):
    # """
    # 注册蓝图
    # :param app:
    # :return:
    # """
    from .app_login import login as login_blueprint
    from .lgbm import analysis as analysis_blueprint
    app.register_blueprint(login_blueprint)
    app.register_blueprint(analysis_blueprint)


def database(app, db):
    # """
    # 初始化数据库
    # :param app:
    # :return:
    # """
    db.init_app(app)
    db.create_all()
    db.session.commit()


def create_app():
    my_app = Flask(__name__,template_folder="templates")
    with my_app.app_context():
        # app注册蓝图
        register_bp(my_app)
        # app加载配置
        my_app.config.from_object(BaseConfig)
        # 数据库管理对象
        database(my_app, db)
        # 用于登录验证
        login_manager.init_app(my_app)
        login_manager.login_view = 'login.login'
    return my_app