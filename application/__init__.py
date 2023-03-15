from flask import Flask, render_template, flash, redirect, url_for
from application.forms import SingUp, Login
from flask_login import current_user, LoginManager, login_user
from application.models import User, Post, Community, db
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'StandWithUkraine'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678990@localhost:5432/alya_redit'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager(app)

@app.before_first_request
def create_tables():
    db.create_all()
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/') #Головна сторінка
@app.route('/index')
def main():
    form = 'Це головна сторінка'
    return render_template('index.html', title='Reddit')


@app.route('/sing_in') #Реєстрація
def sing_up():
    form = SingUp()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email,password_hash=form.password.data )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('authorization/register.html', title='Sing Up', form=form)

@app.route('/log_in', methods=['GET', 'POST']) #вхід на акк
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('authorization/login.html', title='Log In', form=form)

@app.route('/public') #публікація
def public():
    return render_template('public.html', title='Public your reddit')

@app.route('/user/<username>') #декоратор для перегляду профілю
def user(username):
    return render_template('user.html', title=username)

@app.route('/kind/<subreddit>') #Сабреддіт
def kind(subreddit):
    return render_template('kind.html', title='subreddit')