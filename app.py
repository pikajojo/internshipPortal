from flask import request, render_template, redirect, url_for, session, g, Flask
from blueprints.auth import bp as auth_bp
import config
from exts import mail
from flask_mail import Mail

from mongoDb_connection.mongoDb_connection import find_document
# 基本功能完成了，还有一些优化
# homepage.html
# 根据不同role跳转不同的页面
# 新增base.html做统一导航栏，右上角的登录/注册
# 登录页面表单做的好看点
# 写技术文档



app = Flask(__name__, static_url_path="/")

## config for session
app.config['SECRET_KEY'] = "sdfklas0lk42j"

## config for send email verification code
app.config['MAIL_SERVER']= "smtp.qq.com"
app.config['MAIL_USE_SSL']= True
app.config['MAIL_PORT']= 465
app.config['MAIL_USERNAME']= "2476131481@qq.com"
app.config['MAIL_PASSWORD']= "suexjnacipuqebjc"
app.config['MAIL_DEFAULT_SENDER']= "2476131481@qq.com"

mail = Mail(app)
mail.init_app(app)
app.register_blueprint(auth_bp)

# @dataclass
# class User:
#     id: str
#     username: str
#     password: str
#

# users = [
#     User(1, "Admin", "123456"),
#     User(2, "Eason", "888888"),
#     User(3, "Tommy", "666666"),
# ]
@app.route("/")
def homepage():
    return render_template("index.html")

# 勾子函数（感觉是插队函数 hook 装饰器)
@app.before_request
def before_request():
    user_id = session.get("id")
    user_name = session.get("username")
    if user_id:
        user = find_document({"id": user_id})
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)

@app.context_processor
def my_context_processor():
    return{"user":g.user}

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # 登录操作
#         session.pop('user_id', None)
#         username = request.form.get("username", None)
#         password = request.form.get("password", None)
#         user = [u for u in users if u.username == username]
#         if len(user) > 0:
#             user = user[0]
#         if user and user.password == password:
#             session['user_id'] = user.id
#             return redirect(url_for('profile'))
#
#     return render_template("login.html")

# @app.route("/register")
# def register():
#     return render_template("register.html")
# @app.route("/profile")
# def profile():
#     if not g.user:
#         return redirect(url_for('login'))
#
#     return render_template("profile.html")

#
# @app.route("/logout")
# def logout():
#     session.pop("user_id", None)
#     return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)