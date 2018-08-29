from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired

class LoginForm(FlaskForm):
    username = StringField( validators=[DataRequired()], render_kw={"placeholder": "Логин"})
    password = PasswordField( validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class PostForm(FlaskForm):
    title = StringField(validators=[InputRequired()], render_kw={"placeholder": "Заголовок"})
    body = TextAreaField(validators=[InputRequired()], render_kw={"placeholder": "Текст", "spellcheck": "true"})
    date = DateField(format='%Y-%m-%d')
    # tags = SelectField('Теги', choices=[(tag.id, tag.name) for tag in Tag.query.all()])
    submit = SubmitField('Создать')