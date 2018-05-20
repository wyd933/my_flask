from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    user_name = StringField('What is you name', validators=[DataRequired()])
    submit = SubmitField('Submit')