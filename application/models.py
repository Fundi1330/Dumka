from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    tablename = '__User__'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    about_me = db.Column(db.string)


    def __repr__(self) -> str:
        return '<User {}'.format(self.username)

class Post(db.Model):
    tablename = '__Post__'
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String)
    tag = db.Column(db.String, index=True)
    author = db.Column(db.String, index=True)


    def __repr__(self) -> str:
        return '<Post {}'.format(self.body)


class Community(db.Model):
    tablename = '__Community__'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)


    def __repr__(self) -> str:
        return f'name: {self.name}, price: {self.price}'