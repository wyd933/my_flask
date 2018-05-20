from flask import Flask
#flask对象初始化
def create_app():
    app = Flask(__name__)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app