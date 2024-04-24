
from flask import request, render_template, redirect, url_for, session, g, Flask
from blueprints.auth import bp as auth_bp

from flask_mail import Mail
from mongoDb_connection.mongoDb_connection import find_document


# Todo
# homepage.html [不做了]
# 写文档 [慢慢写吧]



app = Flask(__name__, static_url_path="/")
## SECRET_KEY config for session
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



if __name__ == '__main__':
    app.run(debug=True)