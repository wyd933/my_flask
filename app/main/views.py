from flask import render_template
from . import main
#注册主界面蓝本的功能
@main.route('/', methods = ['GET', 'POST'])
def index():
    return '<h1>Hello World</h1>'

@main.route('/user/<name>', methods = ['GET', 'POST'])
def user(name):
    return render_template('hello.html', name=name)