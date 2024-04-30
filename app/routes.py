# app.py 或其他文件
# from .config import Config
from flask import Blueprint, current_app
from .extensions import mongo, fs
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# 现在你可以使用 Config 类来访问 DB 和 FS
# DB = Config.DB
# FS = Config.FS


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


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the login.html form submission here
        # You would typically validate the credentials and log the user in.
        pass
    # Render the login.html templates if it's a GET request or credentials are invalid
    return render_template('login.html')


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

    if request.method == 'POST':
        # 这里处理提交的申请数据
        # 比如：name = request.form['name']
        return redirect(url_for('thank_you'))

    # 对于GET请求，显示申请表单
    return render_template('apply.html', company=company)

@main_blueprint.route('/thank_you')
def thank_you():
    return "感谢您的申请，我们将尽快与您联系！"





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
