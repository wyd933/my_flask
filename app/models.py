from flask import current_app,request
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import hashlib

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

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_role():
        roles = {
            'User': (Permission.ADMINSTER |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator' : (Permission.FOLLOW |
                           Permission.COMMENT |
                           Permission.WRITE_ARTICLES |
                           Permission.MODERATE_COMMENTS, False),
            'Adinistrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
    def has_permission(self, perm):
        self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' %self.name

class User(UserMixin,db.Model):
    #“real customers class”

    #真实用户表名users
    #用户id（主键）和用户名（username）以及在本地所扮演的角色（管理员、版主、普通用户的代表Role）
    #role_id外键、User通过roles的id关联到Role

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Adinistrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()


    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    avatar_hash = db.Column(db.String(32))
    #我们现在的访问一般通过邮箱地址登录、在论坛或贴吧有自己的昵称、表单后续是密码和登录密码
    #数据库中加索引可以加快数据访问速度
    email = db.Column(db.String(64), unique=True, index=True)


    #密码功能
    password_hash = db.Column(db.String(128))

    #用户认证功能
    confirmed = db.Column(db.Boolean, default=False)

    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    avatar_hash = db.Column(db.String(32))

    posts = db.relationship('Post', backref='author', lazy='dynamic')

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

    # def can(self, permissions):
    #     return self.role is not None and (self.permissions & permissions)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMINSTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)


    def gravatar(self, size=100, default='identicon', rating='g'):
        #if request.is_secure:
        url = 'https://secure.gravatar.com/avatar'
        #else:
            #url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(\
            url=url, hash=hash, size=size, default=default, rating=rating)


    def __repr__(self):
        return '<User %r Confirmed %r>' %(self.username, self.confirmed)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_adminstrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
