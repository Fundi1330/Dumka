from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Length
from hashlib import md5


class Registration(FlaskForm):  # Для реєстрації, треба html
    name = StringField('Імя', validators=[DataRequired('Не може бути пусте')])
    nickname = StringField('Користувач', validators=[DataRequired('Не може бути пусте')])
    password = PasswordField('Пароль', validators=[DataRequired('Не може бути пусте')])
    email = StringField('Почта', validators=[DataRequired('Не може бути пусте'), Email()])

    submit = SubmitField('Підтвердити')

class Login(FlaskForm):  # Для входу, треба html
    nickname = StringField('Користувач', validators=[DataRequired('Не може бути пусте')])
    password = PasswordField('Пароль', validators=[DataRequired('Не може бути пусте')])
    submit = SubmitField('Підтвердити')
    remember_me = BooleanField('Запамятай мене!')

class EditForm(FlaskForm):  # Для того щоб миняти імя и тд треба бд
    # бд

    name = StringField('Користувач', validators=[DataRequired('Не може бути пусте')])
    about_me = TextAreaField('Про мене', validators=[Length(min=0, max=500)])
    submit = SubmitField('Підтвердити')  # Кнопка

    def avatar(self, size):
        return """Силка на фото""" + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)


class EditFormPrivat(FlaskForm):  # Теж треба бд
    # бд


    username = StringField('Користувач', validators=[DataRequired('Не може бути пусте')])
    password = PasswordField('Пароль', validators=[DataRequired('Не може бути пусте')])
    email = StringField('Почта', validators=[DataRequired('Не може бути пусте'), Email()])
    submit = SubmitField('Підтвердити')  # Кнопка


class Posts(FlaskForm):  # Треба бд для додавання постів та коментів
    # бд

    title = TextAreaField('Заголовок', validators=[Length(min=0, max=400), DataRequired('Не може бути пусте')])
    posts = TextAreaField('Пост', validators=[Length(min=0, max=1800), DataRequired('Не може бути пусте')])
    tag = TextAreaField('Тег', validators=[Length(min=0, max=200), DataRequired('Не може бути пусте')])
    submit = SubmitField('Підтвердити')

class Comment(FlaskForm):
    comets = TextAreaField('Коментувати', validators=[Length(min=0, max=800), DataRequired('Не може бути пусте')])
    submit = SubmitField('Підтвердити')
