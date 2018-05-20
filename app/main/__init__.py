from flask import Blueprint
#创建一个主界面的蓝本
main = Blueprint("main", __name__)
from . import views
