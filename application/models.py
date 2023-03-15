from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    about_me = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self) -> str:
        return '<User {}'.format(self.username)

class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String)
    tags = db.Column(ARRAY(db.String))
    author = db.Column(db.String, index=True)


    def __repr__(self) -> str:
        return '<Post {}'.format(self.author)


class Community(db.Model):
    __tablename__ = 'Community'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)


    def __repr__(self) -> str:
        return '<Community {}'.format(self.name)