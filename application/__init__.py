from flask import Flask, render_template, flash, redirect, url_for, request
from .forms import Registration, Login, EditForm, EditFormPrivat
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
from sqlalchemy import desc, update

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
    posts = Post.query.order_by(desc(Post.date_of_publication)).all()
    recomended_communities = Community.query.all()
    form = PostForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        tags = findall('[a-z]{1,}|[а-я]{1,}', form.tag.data.lower())
        post = Post(theme=form.title.data, tags=tags, users=current_user, text=form.posts.data, likes=0, date_of_publication=datetime.datetime.now())
        db.session.add(post)
        db.session.commit()
        flash('Пост успішно доданий на сайт!', 'succes')
    elif not current_user.is_authenticated:
        flash('Спочатку вам потрібно зареєструватися!', 'error')
    return render_template('index.html', title='Reddit', posts=posts, recomended_communities=recomended_communities, form=form)


@app.route('/singup', methods=['GET', 'POST']) #Реєстрація
def signup():
    form = Registration()
    if form.validate_on_submit():
        interests = findall('[a-z]{1,}|[а-я]{1,}', form.recomendation.data.lower())
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password_hash=form.password.data, interests=interests)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ви успішно зареєструвалися!', 'succes')
        return redirect(url_for('login'))
    return render_template('authorization/register.html', title='Реєстрація', form=form)

@app.route('/login', methods=['GET', 'POST']) #вхід на акк
def login():
    if current_user.is_authenticated:
       return redirect('index')
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Неправильний логін або пароль", category='error')
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect('index')
    return render_template('authorization/login.html', title='Вхід', form=form)

@app.route('/public') #публікація
def public():
    return render_template('public.html', title='Публікуй свій реддіт')

@app.route('/user/<username>') #декоратор для перегляду профілю
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('users/profile.html', title=username, user=user)

@app.route('/kind/<subreddit>') #Сабреддіт
def kind(subreddit):
    return render_template('kind.html', title='Сабреддіт')

@app.route('/editpost')
def edit_post():
    return render_template('edit_post.html', title='Зміни свій пост')

@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.filter_by(id=id).first()

    if 'delete' in request.form:
        db.session.delete(post)
        db.session.commit()
        flash('пост успішно видалений', 'succes')
        return redirect('/')
    elif 'edit' in request.form:
        return redirect(url_for('/editpost', id=post.id))

    return render_template('posts/post.html', title='Пост', post=post)

@app.route('/faq')
def faq():
    return render_template('footer/faq.html', title='Faq')

@app.route('/about_us')
def about_us():
    return render_template('footer/about_us.html', title="About us")

@app.route('/editform', method=['GET', 'POST'])
def edit_form():
    akkk = User.query.filter_by(id=current_user.id).first()
    form = EditForm()
    if form.validate_on_submit():
        akkk.name = form.name.data
        akkk.about_me = form.about_me.data
        db.session.commit()
    return render_template('edit_form', title='Зміна данних', form=form)

@app.route('/editformprivate', methods=['GET', 'POST'])
def edit_form_privat():
    akkk = User.query.filter_by(id=current_user.id).first()
    form = EditFormPrivat()
    if form.validate_on_submit():
        akkk.username = form.username.data
        akkk.password_hash = akkk.set_password(form.password.data)
        akkk.email = form.email.data
        db.session.commit()
    return render_template('edit_private_form.html', title='Зміна особистих данних', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():


admin.add_view(FileAdmin(path, '/static/', name='files'))
admin.add_view(ModelView(User, db.session, name='Користувачі'))