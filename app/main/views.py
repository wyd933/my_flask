from flask import render_template
from . import main
from datetime import datetime
#注册主界面蓝本的功能
@main.route('/', methods = ['GET', 'POST'])
def index():
    return '<h1>Hello World</h1>'

#如果加入变量，那么变量会把访问的资源全部占用，不推荐这么做？？？？个人想法
# @main.route('/user/<name>', methods = ['GET', 'POST'])
# def user(name):
#     return render_template('hello.html', name=name)

@main.route('/user/bootstrap/<name>', methods = ['GET', 'POST'])
def bootstrap(name):
    return render_template('user_bootstrap.html', name=name, current_time=datetime.utcnow())