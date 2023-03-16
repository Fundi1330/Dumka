from flask import Flask, render_template, flash, redirect, url_for
<<<<<<< HEAD
from application.forms import Registration, Login
from flask_login import current_user, LoginManager, login_user
from application.models import User, Post, Community, db
=======
from .forms import SingUp, Login
from flask_login import current_user, LoginManager, login_user
from .models import User, Posts, Community, db
>>>>>>> 50cb29a (corrected imports)
from flask_migrate import Migrate
from .forms import Posts as PostForm

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


@app.route('/', methods=['GET', 'POST']) #Головна сторінка
@app.route('/index', methods=['GET', 'POST'])
def main():
    posts = Post.query.all()
    recomended_communities = Community.query.all()
    form = PostForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        post = Post(theme=form.title.data, tag=form.tag.data, author=current_user.username)
        db.session.add(post)
        db.session.commit()
    return render_template('index.html', title='Reddit', posts=posts, recomended_communities=recomended_communities, form=form)


@app.route('/sing_in', methods=['GET', 'POST']) #Реєстрація
def sing_up():
    form = Registration()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password_hash=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('log_in'))
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
            return redirect(url_for('log_in'))
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
