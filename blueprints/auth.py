import random
import string
import uuid
from datetime import timedelta

from email_validator import validate_email
from flask_login import login_user

from blueprints.forms import Loginform, RegisterForm
from mongoDb_connection.mongoDb_connection import find_document, insert_document
from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, g
from exts import mail
from flask_mail import Message

bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = Loginform(request.form)
        # 应该换成 邮箱 有唯一性 去搜索对应用户，这个命名有点问题，但是不影响使用
        user_email = find_document({"email": form.email.data})

        if not user_email:
            print("邮箱在数据库中并不存在")
            return redirect(url_for("auth.login"))
        if form.password.data == user_email.get('pwd'):
            # cookie: 存放登录授权
            # session  经过加密后存在cookie
            session['id'] = user_email.get('id')
            ## 加一下角色跳转不同profile
            if user_email.get('role')=='admin':
                return redirect(url_for('auth.profile_admin'))
            elif user_email.get('role')=='staff':
                return redirect(url_for('auth.profile_staff'))
            else:
                return redirect(url_for('auth.profile_student'))
        else:
            print(user_email.get('pwd'))
            print(form.password.data)
            print(str(form.password.data) == user_email.get('pwd'))
            return redirect(url_for("auth.login"))


@bp.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    # 验证用户提交的邮箱和验证码是否对应且正确
    if request.method == 'POST':
        form = RegisterForm(request.form)
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证 flask-wtf:wtforms
        if form.validate():
            if request.form.get('captcha', '') == session.get('captcha', ''):
                # 检查邮箱是否已经被注册
                if find_document({"email":request.form['email']}):
                    return jsonify({'status': 'error', 'message': '该邮箱已经被注册'}), 400
                # 如果邮箱没有被注册过，执行注册逻辑
                # 注册逻辑...
                else:
                    id = str(uuid.uuid4())
                    pwd = form.password.data
                    username = form.username.data
                    role = request.form['role']
                    email = form.email.data

                    user_data = {
                        "id":id,
                        "username": username,
                        "pwd": pwd,
                        "email": email,
                        "role": role
                    }
                    insert_document(user_data)
                    print('注册成功')
                    return redirect('/login')
            else:
                return jsonify({'status': 'error', 'message': '验证码错误'}), 400
        else:
            errors = form.errors
            print(errors)  # 在控制台打印错误信息
            return redirect(url_for('/register'))
        # 表单验证 flask-wtf:wtforms

@bp.route("/profile_admin", methods=['GET'])
def profile_admin():
    return render_template("profiles/profile_admin.html")
    # return "登录成功，进入管理员页面"

@bp.route("/profile_staff", methods=['GET'])
def profile_staff():
    return render_template("profiles/profile_staff.html")
    # return "登录成功，进入老师页面页面"

@bp.route("/profile_student", methods=['GET'])
def profile_student():
    return render_template("profiles/profile_student.html")
    # return "登录成功，进入学生页面"

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route("/captcha/email", methods=['POST', 'GET'])
def get_email_captcha():
    # url使用path传参数
    # /captcha/email/<email>
    # /captcha/email ? email = xxx@qq.com
    email = request.args.get("email")
    # 获取邮件，并发送 4/6为地址，全部为随机数字
    code_source = string.digits * 4
    captcha = random.sample(code_source, 4)
    captcha = "".join(captcha)
    # 先存在session里面
    session["captcha"] = captcha
    message = Message(subject="Internship Portal Verification Code", recipients=[email],
                      body=f"Internship Portal Verification Code {captcha}")
    mail.send(message)
    print(captcha)
    return jsonify({"code": 200, "message": '', "data": None})


# # 验证码校验功能，先写上，再融合
# @bp.route("/verify_captcha", methods=["POST"])
# def verify_captcha():
#     user_captcha = request.form.get("captcha")
#     if "captcha" in session and user_captcha == session["captcha"]:
#         # 验证码正确
#         del session["captcha"]  # 验证成功后删除验证码
#         return jsonify({"success": True})
#     else:
#         # 验证码错误
#         return jsonify({"success": False, "message": "验证码错误"})

# @bp.route("/mail")
# def mail_test():
#     message = Message(subject="Internship Portal Verification Code", recipients=["w5jingyi@gmail.com"],body="test")
#     mail.send(message)
#     return "邮件发送成功"