from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"id": "login",
                                                                                       "class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"id": "password",
                                                                               "class": "form-control"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
