from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class SingUp(FlaskForm):  # Для реєстрації, треба html
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    remember_me = BooleanField('Remember Me!')


class Login(FlaskForm):  # Для входу, треба html
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
