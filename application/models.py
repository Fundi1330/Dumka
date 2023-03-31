from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


user_roles = db.Table("user_roles",
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('Role.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String)
    about_me = db.Column(db.String(500), index=True)
    interests = db.Column(ARRAY(db.String))
    posts = db.relationship('Post', backref='users', lazy='dynamic', primaryjoin="User.username == Post.author")
    avatar = db.Column(db.String, default='default.png')
    active = db.Column(db.Boolean())
    roles = db.relationship('Roles', secondary=user_roles, backref='user', lazy=True)

    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self) -> str:
        return '<User {}'.format(self.username)

class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(60))
    text = db.Column(db.String(4000))
    date_of_publication = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tags = db.Column(ARRAY(db.String))
    author = db.Column(db.String, db.ForeignKey('User.username'), nullable=False)
    likes = db.Column(db.Integer, index=True)
    comments = db.relationship('Comment', backref='comment', lazy='dynamic', primaryjoin='Post.id == Comment.post_id')
    posts = db.Column(db.Integer, db.ForeignKey('Community.id'))

    def __repr__(self) -> str:
        return '<Post {}'.format(self.author)


class Community(db.Model):
    __tablename__ = 'Community'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    description = db.Column(db.String(500), index=True)
    themes = db.Column(ARRAY(db.String))
    community = db.relationship('Post', backref='community', lazy='dynamic')
    avatar = db.Column(db.String, default='communities/default.png')
    author = db.Column(db.String(120))

    def __repr__(self) -> str:
        return '<Community{}'.format(self.name)
    
class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('Post.id'))
    author = db.Column(db.String, index=True)
    text = db.Column(db.String(1500), index=True)
    date_of_publication = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Comment{}'.format(self.author)
    
class Roles(db.Model, RoleMixin):
    __tablename__ = 'Role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f'Role {self.name}'