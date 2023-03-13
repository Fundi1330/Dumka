from flask import Flask, render_template, flash, redirect, url_for
from .forms import SingUp, Login
from flask_login import current_user, LoginManager

app = Flask(__name__)

app.config['SELECT_KEY'] = '1234'


login = LoginManager(app)

@app.route('/') #Головна сторінка
@app.route('/index')
def main():
    form = 'Це головна сторінка'
    return render_template('index.html', form=form)     # треба html файл зробить


@app.route('/sing_in') #Реєстрація
def sing_in():
    return render_template('sing_in.html')  # теж треба html файл зробить

@app.route('/log_in', methods=['GET', 'POST']) #вхід на акк
def log_in():
    return render_template('log_in.html')  #треба html файл зробить

@app.route('/public') #публікація
def public():
    return render_template('public.html')  #треба html файл зробить

@app.route('/user/<username>') #декоратор для перегляду профілю
def user(username):
    return render_template('user.html')

@app.route('/kind/<subreddit>') #Сабреддіт
def kind(subreddit):
    return render_template('kind.html') #Треба html файл