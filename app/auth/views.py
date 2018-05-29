from . import auth
from  flask import render_template
from .form import LoginForm

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)