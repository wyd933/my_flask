from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from datetime import datetime
from .form import NameForm
from ..models import User, Role
from ..import db
from ..email import send_email
#注册主界面蓝本的功能
@main.route('/', methods = ['GET', 'POST'])
def index():
    return '<h1>Hello World</h1>'


#如果加入变量，那么变量会把访问的资源全部占用，不推荐这么做？？？？个人想法
# @main.route('/user/<name>', methods = ['GET', 'POST'])
# def user(name):
#     return render_template('hello.html', name=name)

#其这是一个处理USER的视图函数，把变量保存在和客户端的会话中
#同时还保留了URL的变量访问，不过变量访问应该很占用资源。
@main.route('/user/bootstrap/<name>', methods = ['GET', 'POST'])
def bootstrap(name):
    # user_name = None
    # form = NameForm()
    # if form.validate_on_submit():
    #     user_name = form.user_name.data
    #     form.user_name.data = ''
    # return render_template('user_bootstrap.html', name=name, user_name = user_name, \
    #                        current_time = datetime.utcnow(), form=form,)
    form = NameForm()
    if form.validate_on_submit():
        session['user_name'] = form.user_name.data
        flash('welcome welcome')
        return redirect(url_for('.bootstrap', name=name))
    return render_template('user_bootstrap.html', user_name=session.get('user_name'), \
                            name = name, current_time=datetime.utcnow(), form=form, )

@main.route('/bootstrap', methods = ['GET', 'POST'])
def user_bootstrap():
    form = NameForm()
    if form.validate_on_submit():
        session['user_name'] = form.user_name.data
        return redirect(url_for('.user_bootstrap'))
    return render_template('user_bootstrap.html', user_name = session.get('user_name'), \
                           current_time = datetime.utcnow(), form=form,)

@main.route('/sqlform', methods = ['GET','POST'])
def sql_and_form():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user_name.data).first()
        if user is None:
            user = User(username=form.user_name.data)
            db.session.add(user)
            session['known']=False
            if current_app.config['FLASK_ADMIN']:
                send_email(current_app.config['FLASK_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known']=True
        session['user_name'] = form.user_name.data
        form.user_name.data = ''
        return redirect(url_for('.sql_and_form'))
    return render_template('user_bootstrap.html', user_name = session.get('user_name'),\
                           current_time = datetime.utcnow(), form=form, known=session.get('known', False))