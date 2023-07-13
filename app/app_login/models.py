# """登录需要的数据库模型（用户表）"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from flask import Flask


class User(UserMixin, db.Model):
    # 第一个参数指定字段类型，后面设置属性
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phonenumber = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password,email,phonenumber):
        self.username = username
        self.password = password
        self.email = email
        self.phonenumber = phonenumber

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


