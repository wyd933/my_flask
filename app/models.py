from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' %self.name

class User(UserMixin,db.Model):
    #“real customers class”

    #真实用户表名users
    #用户id（主键）和用户名（username）以及在本地所扮演的角色（管理员、版主、普通用户的代表Role）
    #role_id外键、User通过roles的id关联到Role
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    #我们现在的访问一般通过邮箱地址登录、在论坛或贴吧有自己的昵称、表单后续是密码和登录密码
    #数据库中加索引可以加快数据访问速度
    email = db.Column(db.String(64), unique=True, index=True)


    #密码功能
    password_hash = db.Column(db.String(128))
    #设定密码访问属性
    @property
    def password(self):
        raise AttributeError("password is not a readable(fget) attribute")
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' %self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))