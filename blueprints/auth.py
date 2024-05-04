import random
import string
import uuid
from blueprints.forms import Loginform, RegisterForm
from mongoDb_connection.mongoDb_connection import find_document, insert_document
from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, g
from exts import mail
from flask_mail import Message

bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = Loginform(request.form)
        # email is unique attribute to match user in mongodb
        user_email = find_document({"email": form.email.data})

        if not user_email:
            print("Email doesn't exit! ")
            return redirect(url_for("auth.login"))
        if form.password.data == user_email.get('pwd'):
            # save the user into session
            session['id'] = user_email.get('id')
            ## based on role jump into different profile
            if user_email.get('role') == 'admin':
                return redirect(url_for('auth.profile_admin'))
            elif user_email.get('role') == 'staff':
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
    # Validate code and your input
    if request.method == 'POST':
        # validate Form value
        form = RegisterForm(request.form)
        if form.validate():
            if request.form.get('captcha', '') == session.get('captcha', ''):
                # Validate the email has been existed in database
                if find_document({"email": request.form['email']}):
                    return jsonify({'status': 'error', 'message': 'email has been existed'}), 400
                # if new user, continue register process
                else:
                    # automatically generate the id
                    id = str(uuid.uuid4())
                    pwd = form.password.data
                    username = form.username.data
                    role = request.form['role']
                    email = form.email.data

                    user_data = {
                        "id": id,
                        "username": username,
                        "pwd": pwd,
                        "email": email,
                        "role": role
                    }
                    insert_document(user_data)
                    print('Successfully Register!!')
                    return redirect('/login')
            else:
                return jsonify({'status': 'error', 'message': 'Code error'}), 400
        # if error, stay register.html
        else:
            errors = form.errors
            print(errors)
            return redirect(url_for('/register'))


# different page based on user's role
@bp.route("/profile_admin", methods=['GET'])
def profile_admin():
    return render_template("profiles/profile_admin.html")


@bp.route("/profile_staff", methods=['GET'])
def profile_staff():
    return render_template("profiles/profile_staff.html")


@bp.route("/profile_student", methods=['GET'])
def profile_student():
    return render_template("profiles/profile_student.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# backend for captcha code
# use register.js send request to here
@bp.route("/captcha/email", methods=['POST', 'GET'])
def get_email_captcha():
    # Parameter transfer
    # /captcha/email/<email>
    # /captcha/email ? email = xxx@qq.com
    email = request.args.get("email")
    # 4 randome number
    code_source = string.digits * 4
    captcha = random.sample(code_source, 4)
    captcha = "".join(captcha)
    # save in session
    session["captcha"] = captcha
    message = Message(subject="Internship Portal Verification Code", recipients=[email],
                      body=f"Internship Portal Verification Code {captcha}")
    mail.send(message)
    print(captcha)
    return jsonify({"code": 200, "message": '', "data": None})
