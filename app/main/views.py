from flask import render_template
from . import main
from datetime import datetime
from .form import NameForm
#注册主界面蓝本的功能
@main.route('/', methods = ['GET', 'POST'])
def index():
    return '<h1>Hello World</h1>'

#如果加入变量，那么变量会把访问的资源全部占用，不推荐这么做？？？？个人想法
# @main.route('/user/<name>', methods = ['GET', 'POST'])
# def user(name):
#     return render_template('hello.html', name=name)

#其实不应该放在这里，这是一个处理USER的试图函数
@main.route('/user/bootstrap/<name>', methods = ['GET', 'POST'])
def bootstrap(name):
    user_name = None
    form = NameForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        form.user_name.data = ''
    return render_template('user_bootstrap.html', name=name, user_name = user_name, \
                           current_time = datetime.utcnow(), form=form,)



