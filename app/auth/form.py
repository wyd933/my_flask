from flask_wtf import FlaskForm
from  wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired])
    # user_name = StringField('role_name', validators=[DataRequired])
    remember_me = BooleanField('keep me loggged in')
    submit = SubmitField('Log in')