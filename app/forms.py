from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired
from flask_ckeditor import CKEditorField

class LoginForm(Form):
    username = StringField( validators=[DataRequired()], render_kw={"placeholder": "Логин"})
    password = PasswordField( validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class PostForm(Form):
    title = StringField(validators=[InputRequired()], render_kw={"placeholder": "Заголовок"})
    # body = TextAreaField(validators=[InputRequired()], render_kw={"placeholder": "Текст", "spellcheck": "true"})
    body = CKEditorField('Body')
    date = DateField(format='%Y-%m-%d')
    # tags = SelectField('Теги', choices=[(tag.id, tag.name) for tag in Tag.query.all()])
    submit = SubmitField('Создать')