import wtforms
from wtforms.validators import Email, length, EqualTo
from mongoDb_connection.mongoDb_connection import find_document
from wtforms import Form, StringField, PasswordField, BooleanField, validators

# Form 主要用来验证前端提交数据是否符合要求

# class RegisterForm(wtforms.Form):
#
#     email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
#     username = wtforms.StringField(validators=[length(min=3,max=20,message="用户名格式错误")])
#     password = wtforms.StringField(validators=[length(min=3,max=20,message="密码格式错误")])
#     password_confirm = wtforms.StringField(validators=[EqualTo("password",message="两次密码不一致")])


class RegisterForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(message="Username is required"), validators.Length(min=3, max=20, message="Username must be between 3 and 20 characters")])
    email = StringField('Email', validators=[validators.DataRequired(message="Email is required"), validators.Email(message="Invalid email format")])
    password = PasswordField('Password', validators=[validators.DataRequired(message="Password is required"), validators.Length(min=6, max=20, message="Password must be between 6 and 20 characters")])
    ## password_confirm = PasswordField('Confirm Password', validators=[validators.DataRequired(message="Please confirm your password"), validators.EqualTo('password', message='Passwords must match')])
    captcha = StringField('Verification Code', validators=[validators.DataRequired(message="Verification code is required")])
    ## remember_me = BooleanField('Remember Me')

class Loginform(Form):
    email = StringField('Email', validators=[validators.DataRequired(message="Email is required"),
                                             validators.Email(message="Invalid email format")])
    password = PasswordField('Password', validators=[validators.DataRequired(message="Password is required"),
                                                     validators.Length(min=6, max=20,
                                                                       message="Password must be between 6 and 20 characters")])