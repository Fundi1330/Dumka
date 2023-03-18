from flask import Flask, render_template, flash, redirect, url_for
from .forms import Registration, Login
from flask_login import current_user, LoginManager, login_user, logout_user
from .models import User, Post, Community, db
from flask_migrate import Migrate
from .forms import Posts as PostForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'StandWithUkraine'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dima20+20@localhost:5432/alya_redit'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
path = op.join(op.dirname(__file__), 'static')

db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager(app)

admin = Admin(app, "OP", url='/admin')       #поки без паролю


with app.app_context():
    db.create_all()
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')

@app.route('/', methods=['GET', 'POST']) #Головна сторінка
@app.route('/index/', methods=['GET', 'POST'])
def main():
    posts = Post.query.order_by(Post.date_of_publication).all()
    recomended_communities = Community.query.all()
    form = PostForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        tags = '{' + str(form.tag.data) + '}'
        post = Post(theme=form.title.data, tags=tags, author=current_user.username, text=form.posts.data, likes=0, date_of_publication=datetime.datetime.now())
        db.session.add(post)
        db.session.commit()
        flash('Пост успішно доданий на сайт!')
    return render_template('index.html', title='Reddit', posts=posts, recomended_communities=recomended_communities, form=form)


@app.route('/singup', methods=['GET', 'POST']) #Реєстрація
def signup():
    form = Registration()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password_hash=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('log_in'))
    return render_template('authorization/register.html', title='Sing Up', form=form)

@app.route('/login', methods=['GET', 'POST']) #вхід на акк
def login():
    if current_user.is_authenticated:
       return redirect('index')
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Incorrect login data: check password or username")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect('index')
    return render_template('authorization/login.html', title='Log In', form=form)

@app.route('/public') #публікація
def public():
    return render_template('public.html', title='Public your reddit')

@app.route('/user/<username>') #декоратор для перегляду профілю
def user(username):
    return render_template('users/profile.html', title=username)

@app.route('/kind/<subreddit>') #Сабреддіт
def kind(subreddit):
    return render_template('kind.html', title='subreddit')

@app.route('/post/<post>')
def post(post):
    return render_template('post.html', title='Post')

admin.add_view(FileAdmin(path, '/static/', name='files'))
admin.add_view(ModelView(User, db.session, name='Користувачі'))
