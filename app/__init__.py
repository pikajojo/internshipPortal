from flask import Flask
#from .config import Config
from .extensions import mongo, create_fs


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_random_secret_key_here'
    #app.config.from_object(Config)

    #初始化 PyMongo
    #Initialize PyMongo
    #mongo.init_app(app)

    # 创建 GridFS 对象
    #Create GridFS object
    #with app.app_context():
     #   create_fs(app)

    # 注册蓝图
    #register.html a blueprint
    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app

