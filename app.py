
from flask import  render_template,  session, g, Flask
from blueprints.auth import bp as auth_bp

from flask_mail import Mail
from mongoDb_connection.mongoDb_connection import find_document

app = Flask(__name__, static_url_path="/")
## SECRET_KEY config for session
app.config['SECRET_KEY'] = "sdfklas0lk42j"

## config for send email verification code
app.config['MAIL_SERVER']= "smtp.qq.com"
app.config['MAIL_USE_SSL']= True
app.config['MAIL_PORT']= 465
app.config['MAIL_USERNAME']= "2476131481@qq.com"
## wrong password, correct one in own private repo
app.config['MAIL_PASSWORD']= "--------"
app.config['MAIL_DEFAULT_SENDER']= "2476131481@qq.com"

mail = Mail(app)
mail.init_app(app)
app.register_blueprint(auth_bp)

# setting login as homepage
@app.route("/", methods=['POST', 'GET'])
def homepage():
    return redirect('/login')
    ## return render_template("login.html")

# hook for g.user
@app.before_request
def before_request():
    user_id = session.get("id")
    user_name = session.get("username")
    if user_id:
        user = find_document({"id": user_id})
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)

# return the g.user
@app.context_processor
def my_context_processor():
    return{"user":g.user}


if __name__ == '__main__':
    app.run(debug = True)
