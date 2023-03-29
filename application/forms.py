from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Length
from hashlib import md5
from flask_ckeditor import CKEditorField


class Registration(FlaskForm):  # Для реєстрації, треба html
    name = StringField('Імя', validators=[DataRequired('Не може бути пусте')])
    username = StringField('Користувач', validators=[DataRequired('Не може бути пусте')])
    password = PasswordField('Пароль', validators=[DataRequired('Не може бути пусте')])
    email = StringField('Почта', validators=[DataRequired('Не може бути пусте'), Email()])
    recomendation = StringField('Що вам подобається?', validators=[DataRequired('Наприклад: Футбол, Програмування, Майнкрафт...')])
    submit = SubmitField('Підтвердити')

class LoginForm(FlaskForm):  # Для входу, треба html
    username = StringField('Користувач', validators=[DataRequired('Не може бути пусте')])
    password = PasswordField('Пароль', validators=[DataRequired('Не може бути пусте')])
    remember_me = BooleanField('Запамятай мене!')
    submit = SubmitField('Підтвердити')

class EditForm(FlaskForm):  # Для того щоб миняти імя и тд треба бд
    # бд

    name = StringField("Ім'я", validators=[DataRequired('Не може бути пусте')])
    about_me = CKEditorField('Про мене', validators=[Length(min=0, max=500, message='За над то багато символив')])
    avatar = FileField('Аватарка')  # Аватарка == Назва файла
    submit = SubmitField('Підтвердити')  # Кнопка

    def avatar(self, size):
        return """Силка на фото""" + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)


class EditFormPrivat(FlaskForm):  # Теж треба бд
    # бд
    password = PasswordField('Пароль', validators=[DataRequired('Не може бути пусте')])
    email = StringField('Почта', validators=[DataRequired('Не може бути пусте'), Email(message='Email не існує')])
    submit = SubmitField('Підтвердити')  # Кнопка


class Posts(FlaskForm):  # Треба бд для додавання постів та коментів
    # бд
    title = TextAreaField('Заголовок', validators=[Length(min=0, max=400, message='За над то багато символив'), DataRequired('Не може бути пусте')])
    posts = CKEditorField('Пост', validators=[Length(min=0, max=1800, message='За над то багато символив'), DataRequired('Не може бути пусте')])
    tag = TextAreaField('Теги', validators=[Length(min=0, max=200, message='За над то багато символив'), DataRequired('Не може бути пусте')])
    submit = SubmitField('Підтвердити')

class Comment(FlaskForm):
    comets = TextAreaField('Коментувати', validators=[Length(min=0, max=800, message='За над то багато символив'), DataRequired('Не може бути пусте')])
    submit = SubmitField('Підтвердити')

class Search(FlaskForm):
    search_field = StringField('Пошук', validators=[Length(min=0, max=400, message='За над то багато символив'),
                                              DataRequired('Не може бути пусте')])
    submit = SubmitField('Пошук!')

class Community(FlaskForm):
    name = TextAreaField('Користувач', validators=[DataRequired('Не може бути пусте')])
    tema = TextAreaField('Тема', validators=[Length(min=0, max=400, message='За над то багато символив'),
                                             DataRequired('Не може бути пусте')])
    description = TextAreaField('Опис', validators=[Length(min=0, max=500, message='За над то багато символив'),
                                           DataRequired('Не може бути пусте')])
    photo = FileField('Аватарка')  # Аватарка == Назва файла

    submit = SubmitField('Підтвердити')