from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import Config
#flask对象初始化
bootstrap = Bootstrap()
moment = Moment()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    Config.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app