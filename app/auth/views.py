from . import auth
from  flask import render_template, redirect, url_for, flash, request
from .forms import LoginForm, RegistrationForm
from ..models import User
from flask_login import login_required, logout_user, login_user
from .. import db

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')

    return render_template('auth/login.html', form=form)

@auth.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have logout presently')
    return redirect('main.index')

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.user_name.data, \
                    password = form.password.data)
        db.session.add(user)
        #db.session.commit()
        flash('now youcanlogin')
        return redirect(url_for("auth.login"))
    return render_template('auth/register.html', form=form)