from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, index=True, nullable=False)
    username = db.Column(db.String(120), index=True, unique=True, nullable=False)
    email = db.Column(db.String(60), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    about_me = db.Column(db.String, index=True, nullable=True)
    interests = db.Column(ARRAY(db.String), nullable=False)
    posts = db.relationship('Post', backref='users', lazy='dynamic', primaryjoin="User.username == Post.author", nullable=False)
    avatar = db.Column(db.String, default='default.png', nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self) -> str:
        return '<User {}'.format(self.username)

class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(60), nullable=False)
    text = db.Column(db.String(4000), nullable=False)
    date_of_publication = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    tags = db.Column(ARRAY(db.String), nullable=False)
    author = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    likes = db.Column(db.Integer, index=True, nullable=False)
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')
    posts = db.Column(db.Integer, db.ForeignKey('community.id'))

    def __repr__(self) -> str:
        return '<Post {}'.format(self.author)


class Community(db.Model):
    __tablename__ = 'Community'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, index=True, nullable=False)
    description = db.Column(db.String(300), index=True, nullable=False)
    themes = db.Column(ARRAY(db.String), nullable=False)
    community = db.relationship('Post', backref='community', lazy='dynamic')

    def __repr__(self) -> str:
        return '<Community{}'.format(self.name)

class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.Column(db.String, index=True, nullable=False)
    text = db.Column(db.String(1500), index=True, nullable=False)
    date_of_publication = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return '<Comment{}'.format(self.author)

class Role(db.Model):
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, index=True, nullable=False)
    description = db.Column(db.String, index=True, nullable=False)

User_roles = db.table("User_roles",
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('Role.id'))
)