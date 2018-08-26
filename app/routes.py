from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from app.models import User, Post

from flask_login import current_user, login_user, logout_user
from app.models import User
import pytils


def first_paragraph(body):
    return body[:body.find('\n')] or body

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).limit(5).all()
    for post in posts:
        post.body = first_paragraph(post.body)
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

# @app.route('/<slug>')
# def post_detail(slug):
#     post = Post.query.filter(Post.slug == slug).first_or_404()
#     return render_template('/post.html', post=post)
