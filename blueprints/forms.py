import wtforms
from wtforms.validators import Email, length, EqualTo
from mongoDb_connection.mongoDb_connection import find_document
from wtforms import Form, StringField, PasswordField, BooleanField, validators

# Form used to validate form data
# Form used to validate Register form data
class RegisterForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(message="Username is required"), validators.Length(min=3, max=20, message="Username must be between 3 and 20 characters")])
    email = StringField('Email', validators=[validators.DataRequired(message="Email is required"), validators.Email(message="Invalid email format")])
    password = PasswordField('Password', validators=[validators.DataRequired(message="Password is required"), validators.Length(min=6, max=20, message="Password must be between 6 and 20 characters")])
    captcha = StringField('Verification Code', validators=[validators.DataRequired(message="Verification code is required")])

# Form used to validate Login form data
class Loginform(Form):
    email = StringField('Email', validators=[validators.DataRequired(message="Email is required"),
                                             validators.Email(message="Invalid email format")])
    password = PasswordField('Password', validators=[validators.DataRequired(message="Password is required"),
                                                     validators.Length(min=6, max=20,
                                                                       message="Password must be between 6 and 20 characters")])