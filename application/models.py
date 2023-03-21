from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    about_me = db.Column(db.String, index=True)
    interests = db.Column(ARRAY(db.String))
    posts = db.relationship('Post', backref='users', lazy='dynamic')
    avatar = db.Column(db.String, default='default.png')

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
    author = db.Column(db.String, db.ForeignKey('user.id'))
    likes = db.Column(db.Integer, index=True)


    def __repr__(self) -> str:
        return '<Post {}'.format(self.author)


class Community(db.Model):
    __tablename__ = 'Community'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    description = db.Column(db.String(300), index=True)
    themes = db.Column(ARRAY(db.String))

    def __repr__(self) -> str:
        return '<Community{}'.format(self.name)

class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, index=True)
    author = db.Column(db.String, index=True)
    text = db.Column(db.String(1500), index=True)
    date_of_publication = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Comment{}'.format(self.author)