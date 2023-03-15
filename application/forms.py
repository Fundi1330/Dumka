from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Length
from hashlib import md5

class Registration(FlaskForm):  # Для реєстрації, треба html
    name = StringField('Імя', validators=[DataRequired()])
    username = StringField('Користувач', validators=[DataRequired('Не мже бути пусте')])
    password = PasswordField('Пароль', validators=[DataRequired('Не мже бути пусте')])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    submit = SubmitField('Підтвердити')

class Login(FlaskForm):  # Для входу, треба html
    username = StringField('Користувач', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired('Не мже бути пусте')])
    remember_me = BooleanField('Запамятай мене!')
    submit = SubmitField('Підтвердити')

class EditForm(FlaskForm):  # Для того щоб миняти імя и тд треба бд
    # бд

    name = StringField('Користувач', validators=[DataRequired()])
    about_me = TextAreaField('Про мене', validators=[Length(min=0, max=140)])
    submit = SubmitField('Підтвердити')  # Кнопка


    def avatar(self, size):
        return """Силка на фото""" + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)



class EditFormPrivat(FlaskForm):  # Теж треба бд
    # бд


    username = StringField('Користувач', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired('Не мже бути пусте')])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    submit = SubmitField('Підтвердити')  # Кнопка


class Posts(FlaskForm):  # Треба бд для додавання постів та коментів
    # бд

    title = TextAreaField('Заголовок', validators=[Length(min=0, max=130)])
    posts = TextAreaField('Пост', validators=[Length(min=0, max=350)])
    tag = TextAreaField('Тег', validators=[Length(min=0, max=100)])
    submit = SubmitField('Підтвердити')

class Comment(FlaskForm):
    comets = TextAreaField('Коментувати', validators=[Length(min=0, max=300)])
    submit = SubmitField('Підтвердити')
