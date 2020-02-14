from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, Field
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired('Это поле обязательно')], render_kw={"placeholder": "Логин"})
    password = PasswordField(validators=[InputRequired('Это поле обязательно')], render_kw={"placeholder": "Пароль"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[InputRequired('Это поле обязательно')], render_kw={"placeholder": "Введите заголовок поста"})
    body = CKEditorField("Текст", validators=[InputRequired('Это поле обязательно')])
    timestamp = DateField("Дата", format='%Y-%m-%d', default=datetime.today)
    tags = SelectMultipleField("Теги", coerce=int)
    add_tag = SubmitField('Добавить')
    submit = SubmitField('Создать')


class TagForm(FlaskForm):
    name = StringField("Название тега", validators=[InputRequired()])
    color = StringField("Цвет тега", render_kw={"type": "color", "value": "#0e80c0"})
    submit = SubmitField('Создать')
