# """登录视图的蓝图"""
from flask import Blueprint

login = Blueprint("login", __name__)
from . import view