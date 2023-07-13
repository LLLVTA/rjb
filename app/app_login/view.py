# """登录的视图函数"""
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, login_user
from . import login
from .models import User
from app import login_manager


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象

@login_required
@login.route('/', methods=['GET', 'POST'])
@login.route('/index',methods=['GET','POST'])
# @login_required
def index():
    if request.method == "GET":
        return render_template('index.html')


@login.route('/register', methods=['GET', 'POST'])
def register():
    # 如果请求为post
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phonenumber = request.form.get('phonenumber')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        from app import db
        if not username or not password:
            print(1)
            flash('无效输入')
            return redirect(url_for('login.register)'))
        user = User.query.filter_by(phonenumber=phonenumber).first()
        print(user)
        if not user:
            if password == repassword:
                user = User(username, password,email,phonenumber)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('注册成功')
                return redirect(url_for('login.login'))
            else:
                flash('两次密码不一致')
                return redirect(url_for('login.register'))
        else:
            flash('该手机号已被注册过！')
            return redirect(url_for('login.register'))
    # 请求为get
    return render_template('register.html')


@login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        phonenumber = request.form.get('phonenumber')
        password = request.form.get('password')
        print(phonenumber, password)
        if not phonenumber or not password:
            print('无效的输入')
            return redirect(url_for('login.login)'))
        user = User.query.filter_by(phonenumber=phonenumber).first()
        if not user:
            print("用户不存在")
            return redirect(url_for('login.login'))
        if phonenumber == user.phonenumber:
            if user.check_password(password) or user.password==password:
                login_user(user)  # 登入用户
                print('登录成功')
                return redirect(url_for('login.index'))  # 重定向到主页

        print('用户名或密码错误')  # 如果验证失败，显示错误消息
        return redirect(url_for('login.login'))  # 重定向回登录页面
    return render_template('login.html')
