from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from datetime import datetime
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm
from ..models import User, Role, Permission, Post
from ..import db
from ..email import send_email
from flask_login import login_required, current_user
from ..decorators import admin_required

# #注册主界面蓝本的功能
# @main.route('/', methods = ['GET', 'POST'])
# def index():
#     #return '<h1>Hello World</h1>'
#     return render_template('index.html')

#如果加入变量，那么变量会把访问的资源全部占用，不推荐这么做？？？？个人想法
# @main.route('/user/<name>', methods = ['GET', 'POST'])
# def user(name):
#     return render_template('hello.html', name=name)

#其这是一个处理USER的视图函数，把变量保存在和客户端的会话中
#同时还保留了URL的变量访问，不过变量访问应该很占用资源。
@main.route('/user/bootstrap/<name>', methods = ['GET', 'POST'])
def bootstrap(name):
    # user_name = None'Permission' is undefined
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
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.lacation.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your Profile has been update')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.lacation.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been update')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
        form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return  redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)


