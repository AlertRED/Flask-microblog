from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, PostForm
from app.models import User, Post

from flask_login import current_user, login_user, logout_user
from app.models import User
import pytils

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()
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

@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if current_user.is_authenticated and current_user.username =='ieaiaio':
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            print(title, body)
            try:
                post = Post(title=title, body=body)#, tags=[tag]
                db.session.add(post)
                db.session.commit()
            except Exception as e:
                flash(str(e), 'alert')
            else:
                flash('Пост успешно выложен','success')
            return redirect(url_for('index'))
        form = PostForm()
        return render_template('create_post.html', form=form)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if current_user.is_authenticated and logout_user():
        flash('Выход выполнен успешно', 'success')
    return redirect(url_for('index'))

@app.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('/post.html', post=post)
