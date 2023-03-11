from flask import Flask, render_template

app = Flask(__name__)

app.config['SELECT_KEY'] = '1234'

@app.route('/') #Головна сторінка
def golovna():
    form = 'Це головна сторінка'
    return render_template('index.html', form=form)     #тут Христині треба html файл зробить


@app.route('/sing_in') #Реєстрація
def sing_in():
    return render_template('sing_in.html')  #тут Христині теж треба html файл зробить

@app.route('/log_in') #вхід на акк
def log_in():
    return render_template('log_in.html')  #тут Христині треба html файл зробить

@app.route('/public') #публікація
def public():
    return render_template('public.html')  # тут Христині треба html файл зробить

@app.route('/user/<username>') #декоратор для перегляду профілю
def user(username):
    return render_template('user.html')