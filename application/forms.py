from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Length
from hashlib import md5


class SingUp(FlaskForm):  # Для реєстрації, треба html
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired('Не мже бути пусте')])
    password = PasswordField('Password', validators=[DataRequired('Не мже бути пусте')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    remember_me = BooleanField('Remember Me!')


class Login(FlaskForm):  # Для входу, треба html
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired('Не мже бути пусте')])


class EditForm(FlaskForm):  # Для того щоб миняти імя и тд треба бд
    #бд


    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')  # Кнопка

    def avatar(self, size):
        return """Силка на фото""" + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)


class EditFormprivat(FlaskForm):  # Теж треба бд
    #бд


    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired('Не мже бути пусте')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')  # Кнопка


class Posts(FlaskForm):     #Треба бд для додавання постів та коментів
    # бд

    title = TextAreaField('Title', validators=[Length(min=0, max=130)])
    posts = TextAreaField('Post', validators=[Length(min=0, max=350)])
    tag = TextAreaField('Tag', validators=Length(min=0, max=100))


class Comment(FlaskForm):
    comets = TextAreaField('Comment', validators=[Length(min=0, max=300)])
