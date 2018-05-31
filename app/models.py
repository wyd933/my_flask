from flask import current_app
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Permission:
    FOLLOW               = 0x01
    COMMENT              = 0x02
    WRITE_ARTICLES       = 0x04
    MODERATE_COMMENTS    = 0x08
    ADMINSTER            = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    default = db.Column(db.Boolean, default=False, index=True)
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

    #用户认证功能
    confirmed = db.Column(db.Boolean, default=False)

    #设定密码访问属性
    @property
    def password(self):
        raise AttributeError("password is not a readable(fget) attribute")
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm' : self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r Confirmed %r>' %(self.username, self.confirmed)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))