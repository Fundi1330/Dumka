from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Length
from hashlib import md5


<<<<<<< HEAD
class SingUp(FlaskForm):  # Для реєстрації, треба html
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


class Login(FlaskForm):  # Для входу, треба html
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me!')
    submit = SubmitField('Submit')


class EditForm(FlaskForm):  # Для того щоб миняти імя и тд треба бд
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')  # Button
=======
class Registration(FlaskForm):  # Для реєстрації, треба html
    name = StringField('Імя', validators=[DataRequired()])
    nickname = StringField('Користувач', validators=[DataRequired('Не мже бути пусте')])
    password = PasswordField('Пароль', validators=[DataRequired('Не мже бути пусте')])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    remember_me = BooleanField('Запамятай мене!')
    submit = SubmitField('Підтвердити')

class Login(FlaskForm):  # Для входу, треба html
    nickname = StringField('Користувач', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired('Не мже бути пусте')])
    submit = SubmitField('Підтвердити')

class EditForm(FlaskForm):  # Для того щоб миняти імя и тд треба бд
    # бд

    nickname = StringField('Користувач', validators=[DataRequired()])
    about_me = TextAreaField('Про мене', validators=[Length(min=0, max=140)])
    submit = SubmitField('Підтвердити')  # Кнопка
>>>>>>> 413dc29 (SubmitField)

    def avatar(self, size):
        return """Силка на фото""" + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)


<<<<<<< HEAD
class EditFormprivat(FlaskForm):  # Теж треба бд
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')  # Button
=======
class EditFormPrivat(FlaskForm):  # Теж треба бд
    # бд


    nickname = StringField('Користувач', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired('Не мже бути пусте')])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    submit = SubmitField('Підтвердити')  # Кнопка


class Posts(FlaskForm):  # Треба бд для додавання постів та коментів
    # бд

    title = TextAreaField('Заголовок', validators=[Length(min=0, max=130)])
    posts = TextAreaField('Пост', validators=[Length(min=0, max=350)])
    tag = TextAreaField('Тег', validators=Length(min=0, max=100))
    submit = SubmitField('Підтвердити')

class Comment(FlaskForm):
    comets = TextAreaField('Коментувати', validators=[Length(min=0, max=300)])
    submit = SubmitField('Підтвердити')
>>>>>>> 413dc29 (SubmitField)
