from flask import Flask, render_template, flash, redirect, url_for
from .forms import Registration, Login
from flask_login import current_user, LoginManager, login_user
from .models import User, Post, Community, db
from flask_migrate import Migrate
from .forms import Posts as PostForm
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
app = Flask(__name__)
app.config['SECRET_KEY'] = 'StandWithUkraine'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dima20+20@localhost:5432/alya_redit'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
path = op.join(op.dirname(__file__), 'admin')

db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager(app)



admin = Admin(app, "OP", url='/admin')


with app.app_context():
    db.create_all()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/') #Головна сторінка
@app.route('/index')
def main():
    posts = Post.query.all()
    recomended_communities = Community.query.all()  #рек
    form = PostForm()
    if form.validate_on_submit():
        post = Post(theme=form.title.data, tag=form.tag.data, author=current_user.username)
        db.session.add(post)
        db.session.commit()
    return render_template('index.html', title='Reddit', post=posts, recomended_communities=recomended_communities, form=form)


@app.route('/SingUp', methods=['GET', 'POST']) #Реєстрація
def SignUp():
    form = Registration()
    if form.validate_on_submit():
        user = Registration(username=form.nickname.data, email=form.email.data, password_hash=form.password.data )
        user.set_password(form.password.data)  #тут чогось set_password Жовтим світиться, поки розбиратися не хочу
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('log_in'))
    return render_template('authorization/register.html', title='Sing Up', form=form)

@app.route('/Login', methods=['GET', 'POST']) #вхід на акк
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Registration()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.nickname.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('log_in'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('authorization/login.html', title='Log In', form=form)

@app.route('/public',methods=['GET', 'POST'] ) #публікація
def public():
    return render_template('public.html', title='Public your reddit')

@app.route('/user/<username>') #декоратор для перегляду профілю
def user(username):
    return render_template('user.html', title=username)

@app.route('/kind/<subreddit>') #Сабреддіт
def kind(subreddit):
    return render_template('kind.html', title='subreddit')

admin.add_view(FileAdmin(path, '/admin/', name='files'))
