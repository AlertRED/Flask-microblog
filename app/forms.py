from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={"placeholder": "Логин"})
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class PostForm(FlaskForm):
    title = StringField(validators=[InputRequired()], render_kw={"placeholder": "Заголовок"})
    body = CKEditorField('Body', validators=[DataRequired()])
    # timestamp = DateField(format='%Y-%m-%d', default=datetime.today)
    # tags = StringField(validators=[InputRequired()], render_kw={"placeholder": "Теги"})
    add_tag = SubmitField('Добавить')
    submit = SubmitField('Создать')
