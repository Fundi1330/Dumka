from flask import Flask, render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, LoginManager, login_user, logout_user
from .models import User, Post, Community, db, Comment
from flask_migrate import Migrate
from .forms import Posts as PostForm, EditForm, EditFormPrivat, Registration, Login, Search
from .forms import Comment as CommentForm
from .forms import Community as CommunityForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
import datetime
from re import findall
from sqlalchemy import desc
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'StandWithUkraine'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678990@localhost:5432/alya_redit'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
ckeditor = CKEditor(app)
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
    communities = Community.query.all()
    recomended_communities = []
    form = PostForm()
    if current_user.is_authenticated:
        for i in communities:
            for a in i.themes:
                if a in current_user.interests and i not in recomended_communities and len(recomended_communities) != 5:
                    recomended_communities.append(i)
    if form.validate_on_submit() and current_user.is_authenticated:
        tags = findall('[a-z]{1,}|[а-їґ]{1,}', form.tag.data.lower())
        post = Post(theme=form.title.data, tags=tags, users=current_user, text=form.posts.data, likes=0, date_of_publication=datetime.datetime.now(), comments=[])
        db.session.add(post)
        db.session.commit()
        flash('Пост успішно доданий на сайт!', 'succes')
    elif not current_user.is_authenticated and form.validate_on_submit():
        flash('Спочатку вам потрібно зареєструватися!', 'error')
    return render_template('index.html', title='Reddit', posts=posts, recomended_communities=recomended_communities, form=form)


@app.route('/singup', methods=['GET', 'POST']) #Реєстрація
def signup():
    form = Registration()
    if form.validate_on_submit():
        interests = findall('[a-z]{1,}|[а-їґ]{1,}', form.recomendation.data.lower())
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
    posts = Post.query.filter_by(author=username).order_by(desc(Post.date_of_publication)).all()
    return render_template('users/profile.html', title=username, user=user, posts=posts)

@app.route('/kind/<subreddit>') #Сабреддіт
def kind(subreddit):
    return render_template('kind.html', title='Сабреддіт')

@app.route('/editpost/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    form_P = PostForm()
    post = Post.query.filter_by(id=id).first()
    if current_user.username != post.author:
        abort(404)
    if request.method == 'GET':
        form_P.title.data = post.theme
        form_P.posts.data = post.text
        form_P.tag.data = ', '.join(post.tags)
    if form_P.validate_on_submit():
        post.theme = form_P.title.data
        post.text = form_P.posts.data
        tags = findall('[a-z]{1,}|[а-їґ]{1,}', form_P.tag.data.lower())
        post.tags = tags
        db.session.commit()
        return redirect('/index')
    return render_template('posts/edit_post.html', title='Зміни свій пост', form=form_P, post=post)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.filter_by(id=id).first()
    comments = post.comments
    ordered_comments = comments.order_by(desc(Comment.date_of_publication))
    form = CommentForm()

    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(author=current_user.username, text=form.comets.data, date_of_publication=datetime.datetime.now(), post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Комментар успішно доданий на сайт!', 'succes')
    elif not current_user.is_authenticated and form.validate_on_submit():
        flash('Спочатку вам потрібно зареєструватися!', 'error')

    if 'delete' in request.form:
        db.session.delete(post)
        db.session.commit()
        flash('пост успішно видалений', 'succes')
        return redirect('/')
    elif 'edit' in request.form:
        return redirect(url_for('edit_post', id=post.id))

    return render_template('posts/post.html', title='Пост', post=post, form=form, comments=ordered_comments)

@app.route('/faq')
def faq():
    return render_template('footer/faq.html', title='Faq')

@app.route('/about_us')
def about_us():
    return render_template('footer/about_us.html', title="About us")

@app.route('/editform', methods=['GET', 'POST'])
def edit_form():
    user = User.query.filter_by(id=current_user.id).first()
    form_EF = EditForm()
    if request.method == 'GET':
        form_EF.name.data = user.name
        form_EF.about_me.data = user.about_me

    if form_EF.validate_on_submit():
        user.name = form_EF.name.data
        user.about_me = form_EF.about_me.data
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    return render_template('users/edit_profile.html', title='Зміна данних', form=form_EF)

@app.route('/editformprivate', methods=['GET', 'POST'])
def edit_form_privat():
    user = User.query.filter_by(id=current_user.id).first()
    form_EFP = EditFormPrivat()
    if request.method == 'GET':
        form_EFP.email.data = user.email
        form_EFP.password.data = user.check_password(user.password_hash)

    if form_EFP.validate_on_submit():
        user.password_hash = user.set_password(form_EFP.password.data)
        user.email = form_EFP.email.data
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    return render_template('users/edit_private_data.html', title='Зміна особистих данних', form=form_EFP)

@app.route('/search', methods=['POST', 'GET'])
def search():
    form = Search()
    text_theme2 = []
    if form.validate_on_submit():
        text = Post.query.filter(Post.text.match('%' + form.search_field.data + '%')).all()
        theme = Post.query.filter(Post.theme.match('%' + form.search_field.data + '%')).all()
        if text != []:
            for i in text:
                text_theme2.append(i)
        if theme != []:
            for i in theme:
                if i not in text_theme2:
                    text_theme2.append(i)

        if text_theme2 == []:
            flash('За вашим запитом нічого не зднайдено', 'error')

        flash(text_theme2, 'succes')
        flash(theme, 'succes')
        flash(text, 'succes')



    return render_template('search.html', form=form, title='Пошук', text_theme=text_theme2)


@app.route('/addcommunity', methods=['GET', 'POST'])
def add_community():
    form = CommunityForm()
    if form.validate_on_submit():
        coommunity = CommunityForm(name=form.name.data, description=form.description.data, themes=form.tema.data)
        db.session.add(coommunity)
        db.session.commit()

admin.add_view(FileAdmin(path, '/static/', name='files'))
admin.add_view(ModelView(User, db.session, name='Користувачі'))
