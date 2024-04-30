# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ApplicationForm(FlaskForm):
    student_name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    proposal = TextAreaField('Proposal', validators=[DataRequired()])
    submit = SubmitField('Apply')

