from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Length


class Registration(FlaskForm):  # Для реєстрації, треба html
    name = StringField('Імя', validators=[DataRequired('Не може бути пусте')])
    nickname = StringField('Користувач', validators=[DataRequired('Не може бути пусте')])
    password = PasswordField('Пароль', validators=[DataRequired('Не може бути пусте')])
    email = StringField('Почта', validators=[DataRequired('Не може бути пусте'), Email(message='Email не існує')])
    recomendation = StringField('Що вам подобається?',
                                validators=[DataRequired('Наприклад: Футбол, Програмування, Мйнкрафт...')])
    submit = SubmitField('Підтвердити')


class Login(FlaskForm):  # Для входу, треба html
    nickname = StringField('Користувач', validators=[DataRequired('Не може бути пусте')])
    password = PasswordField('Пароль', validators=[DataRequired('Не може бути пусте')])
    submit = SubmitField('Підтвердити')
    remember_me = BooleanField('Запамятай мене!')


class EditForm(FlaskForm):  # Для того щоб миняти імя и тд треба бд
    # бд

    name = StringField('Користувач', validators=[DataRequired('Не може бути пусте')])
    about_me = TextAreaField('Про мене', validators=[Length(min=0, max=500, message='За над то багато символив')])
    submit = SubmitField('Підтвердити')  # Кнопка
    avatar = FileField('!')  # ! == Назва файла


class EditFormPrivat(FlaskForm):  # Теж треба бд
    # бд

    username = StringField('Користувач', validators=[DataRequired('Не може бути пусте')])
    password = PasswordField('Пароль', validators=[DataRequired('Не може бути пусте')])
    email = StringField('Почта', validators=[DataRequired('Не може бути пусте'), Email(message='Email не існує')])
    submit = SubmitField('Підтвердити')  # Кнопка


class Posts(FlaskForm):  # Треба бд для додавання постів та коментів
    # бд

    title = TextAreaField('Заголовок', validators=[Length(min=0, max=400, message='За над то багато символив'),
                                                   DataRequired('Не може бути пусте')])
    posts = TextAreaField('Пост', validators=[Length(min=0, max=1800, message='За над то багато символив'),
                                              DataRequired('Не може бути пусте')])
    tag = TextAreaField('Тег', validators=[Length(min=0, max=200, message='За над то багато символив'),
                                           DataRequired('Не може бути пусте')])
    submit = SubmitField('Підтвердити')


class Comment(FlaskForm):
    comets = TextAreaField('Коментувати', validators=[Length(min=0, max=800, message='За над то багато символив'),
                                                      DataRequired('Не може бути пусте')])
    submit = SubmitField('Підтвердити')


class Search(FlaskForm):
    search = StringField('Пошук', validators=[Length(min=0, max=400, message='За над то багато символив'),
                                              DataRequired('Не може бути пусте')])


class Community(FlaskForm):
    name = TextAreaField('Користувач', validators=[DataRequired('Не може бути пусте')])
    tema = TextAreaField('Тема', validators=[Length(min=0, max=400, message='За над то багато символив'),
                                             DataRequired('Не може бути пусте')])
    description = TextAreaField('Опис', validators=[Length(min=0, max=500, message='За над то багато символив'),
                                           DataRequired('Не може бути пусте')])
    submit = SubmitField('Підтвердити')


class EditCommunity(FlaskForm):
    name = TextAreaField('Користувач', validators=[DataRequired('Не може бути пусте')])
    tema = TextAreaField('Тема', validators=[Length(min=0, max=400, message='За над то багато символив'),
                                             DataRequired('Не може бути пусте')])
    description = TextAreaField('Опис', validators=[Length(min=0, max=500, message='За над то багато символив'),
                                           DataRequired('Не може бути пусте')])
    submit = SubmitField('Підтвердити')

