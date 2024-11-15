from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from datetime import datetime
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(),
        Length(min=6, message='Имя пользователя должно быть не менее 6 символов')])
    email = StringField('Email', validators=[DataRequired(), Email(),
        Length(min=6, message='Email должен быть не менее 6 символов')])
    password = PasswordField('Пароль', validators=[DataRequired(),
        Length(min=6, message='Пароль должен быть не менее 6 символов')])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message="Пароль и повтор пароля должны совпадать"),
        Length(min=6, message='Пароль должен быть не менее 6 символов')])
    submit = SubmitField('Зарегистрироваться')


class PostForm(FlaskForm):
    title = StringField('Заголовок поста', validators=[DataRequired()])
    content = TextAreaField('Содержание поста', validators=[DataRequired()])
    photos = FileField('Фото', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')])
    submit = SubmitField('Опубликовать')
