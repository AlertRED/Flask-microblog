from app import app, support
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.models import User, Post

from flask_login import current_user, login_user, logout_user

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.filter(Post.is_active).order_by(Post.timestamp.desc()).limit(5).all()
    for post in posts:
        post.body = support.first_paragraph(post.body)
    return render_template('index.html', posts=posts)


@app.route('/mypanel', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль', 'alert')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Вход выполнен успешно', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated and logout_user():
        flash('Выход выполнен успешно', 'success')
    return redirect(url_for('index'))

