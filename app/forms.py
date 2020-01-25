from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={"placeholder": "Логин"})
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[InputRequired()], render_kw={"placeholder": "Введите заголовок поста"})
    body = CKEditorField("Текст", validators=[DataRequired()])
    # timestamp = DateField(format='%Y-%m-%d', default=datetime.today)
    labels = SelectMultipleField("Метки")
    add_tag = SubmitField('Добавить')
    submit = SubmitField('Создать')
