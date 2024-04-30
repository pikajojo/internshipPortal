# app.py 或其他文件
# from .config import Config
from flask import Blueprint, current_app
from .extensions import mongo, fs
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# 现在你可以使用 Config 类来访问 DB 和 FS
# DB = Config.DB
# FS = Config.FS
from flask import render_template, flash, redirect, url_for, session
from app.forms import LoginForm, ApplicationForm
from flask import request, redirect, url_for, render_template, flash
from .model import Application, db


# 创建一个蓝图对象，名为 'main'
# create a blueprint object，called 'main'
main_blueprint = Blueprint('main', __name__, template_folder='../templates')


# 使用该蓝图对象定义路由
# use this blueprint object to define route
@main_blueprint.route('/')
def home():
    # Redirect to the login.html page as the new home page
    return "Welcome to internship portal! Have a nice day!"
    # return redirect(url_for('main.login.html'))

@main_blueprint.route('/student_home')
def student_home():
    #if 'role' in session and session['role'] == 'student':
        #return render_template('student_home.html')
    return "student home"

    #return redirect(url_for('login'))

@main_blueprint.route('/company_home')
def company_home():
    #if 'role' in session and session['role'] == 'company':
    #    return render_template('company_home.html')
    #return redirect(url_for('login'))
    return "company home"

@main_blueprint.route('/instructor_home')
def instructor_home():
    #if 'role' in session and session['role'] == 'instructor':
    #    return render_template('instructor_home.html')
    #return redirect(url_for('login'))
    return "instructor home"



@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'student' and form.password.data == 'iamstudent':
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.student_home'))
        elif form.username.data == 'company' and form.password.data == 'iamcompany':
                flash('You have been logged in!', 'success')
                return redirect(url_for('main.company_home'))
        elif form.username.data == 'instructor' and form.password.data == 'iaminstructor':
                flash('You have been logged in!', 'success')
                return redirect(url_for('main.instructor_home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process the registration form submission here
        # You would typically create a new user account.
        pass
    # Render the register.html templates if it's a GET request or registration details are invalid
    return render_template('register.html')



# 模拟数据
companies = [
    {'name': 'Google', 'id': 1, 'url': 'http://www.google.com/careers'},
    {'name': 'Facebook', 'id': 2, 'url': 'http://www.facebook.com/careers'},
    {'name': 'Amazon', 'id': 3, 'url': 'http://www.amazon.jobs'}
]

@main_blueprint.route('/company', methods=['GET', 'POST'])
def company():
    return render_template('company.html', companies=companies)





@main_blueprint.route('/apply/<int:company_id>', methods=['GET', 'POST'])
def apply(company_id):
    company = next((c for c in companies if c['id'] == company_id), None)
    if company is None:
        return "Company not found", 404

    form = ApplicationForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_application = Application(
            student_name=form.student_name.data,
            student_email=form.student_email.data,
            proposal=form.proposal.data,
            company_name=company['name']
        )
        db.session.add(new_application)
        db.session.commit()
        flash('Application submitted successfully!')
        return redirect(url_for('thank_you'))

    return render_template('apply.html', form=form, company=company)


@main_blueprint.route('/thank_you')
def thank_you():
    return "Thanks for your application, we will contact you soon!"


@main_blueprint.route('/files')
def list_files():
    file_list = fs.list()
    return str(list(file_list))


@main_blueprint.route('/add_file')
def add_file():
    with current_app.open_resource('yourfile.txt', 'rb') as f:
        contents = f.read()
        fs.put(contents, filename='yourfile.txt')
    return "File added!"
