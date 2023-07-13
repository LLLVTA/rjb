# """启动文件"""
from app import create_app
from flask import render_template, session

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)