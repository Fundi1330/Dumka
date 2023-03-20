from flask import Flask, render_template, flash, redirect, url_for, request
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
from re import findall

app = Flask(__name__)
app.config['SECRET_KEY'] = 'StandWithUkraine'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678990@localhost:5432/alya_redit'
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
        tags = findall('[a-z]{1,}|[a-z]{1,}\s[a-z]{1,}', form.tag.data.lower())

        post = Post(theme=form.title.data, tags=tags, author=current_user.username, text=form.posts.data, likes=0, date_of_publication=datetime.datetime.now())
        db.session.add(post)
        db.session.commit()
        flash('Пост успішно доданий на сайт!')
    elif not current_user.is_authenticated:
        flash('Спочатку вам потрібно зареєструватися!')
    return render_template('index.html', title='Reddit', posts=posts, recomended_communities=recomended_communities, form=form)


@app.route('/singup', methods=['GET', 'POST']) #Реєстрація
def signup():
    form = Registration()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password_hash=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('authorization/register.html', title='Sing Up', form=form)

@app.route('/login', methods=['GET', 'POST']) #вхід на акк
def login():
    if current_user.is_authenticated:
       return redirect('index')
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Неправильний логін або пароль")
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

@app.route('/editpost/<int:id>')
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    form = PostForm()
    
    return render_template('edit_post', title='Edit your post', form=form)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.filter_by(id=id).first()

    if 'delete' in request.form:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    elif 'edit' in request.form:
        return redirect('/editpost')

    return render_template('posts/post.html', title='Post', post=post)

@app.route('/faq')
def faq():
    return render_template('footer/faq.html', title='Faq')

@app.route('/about_us')
def about_us():
    return render_template('footer/about_us.html', title="About us")

admin.add_view(FileAdmin(path, '/static/', name='files'))
admin.add_view(ModelView(User, db.session, name='Користувачі'))
