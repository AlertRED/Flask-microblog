from functools import wraps

from flask import render_template, Blueprint, request, flash, redirect, url_for
from app.models import Post, Tag
from app import db, support
from flask_login import current_user, login_required
from app.forms import PostForm

posts = Blueprint('posts', __name__, template_folder='templates')


def admin_only(foo):
    @wraps(foo)
    def check_is_admin(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Вы не авторизованы', 'alert')
            return redirect(url_for('login'))
        if not current_user.check_role('Admin'):
            flash('У вас не достаточно прав', 'alert')
            return redirect(url_for('index'))
        return foo(*args, **kwargs)
    return check_is_admin


@posts.route('/create_post', methods=['POST', 'GET'])
@admin_only
def create_post():
    if request.method == 'POST':
        title, body, timestamp = request.form['title'], request.form['body'], request.form['timestamp']
        try:
            Post.create(title=title, body=body, timestamp=timestamp)  # , tags=[tag]
        except Exception as e:
            flash(str(e), 'alert')
        else:
            flash('Пост успешно выложен', 'success')
        return redirect(url_for('index'))
    form = PostForm()
    return render_template('edit_post.html', form=form, title='Создание поста', button='Создать')


@posts.route('/<slug>', methods=['GET'])
def post_detail(slug):
    post = Post.get_first(slug=slug)
    return render_template('post_detail.html', post=post)


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@admin_only
def edit_post(slug):
    post = Post.get_first(slug=slug)
    if request.method == 'POST':
        form = PostForm(formdate=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for("posts.post_detail", slug=post.slug))
    form = PostForm(obj=post)
    return render_template('edit_post.html', post=post, form=form, title='Изменение поста', button='Сохранить')


@posts.route('/<slug>/restore/', methods=['POST', 'GET'])
@admin_only
def restore(slug):
    if request.method == 'POST':
        return redirect(url_for("index"))
    post = Post.get_first(slug=slug)
    if post:
        post.update(is_active=True)
        flash('Пост восстановлен', 'success')
    return redirect(url_for("posts.basket"))


@posts.route('/<slug>/to_basket/', methods=['POST', 'GET'])
@admin_only
def to_basket(slug):
    if request.method == 'POST':
        return redirect(url_for("index"))
    post = Post.get_first(slug=slug)
    if post:
        post.delete()
        flash('Пост отправлен в корзину', 'success')
    return redirect(url_for("index"))


@posts.route('/<slug>/delete/', methods=['POST', 'GET'])
@admin_only
def delete(slug):
    if request.method == 'POST':
        return redirect(url_for("index"))
    post = Post.get_first(slug=slug)
    if post:
        post.destroy()
    flash('Пост успешно удален', 'success')
    return redirect(url_for("posts.basket"))


@posts.route('/')
def all_posts():
    posts = Post.get(is_active=True)
    for post in posts:
        post.body = support.first_paragraph(post.body)
    return render_template('all_posts.html', posts=posts)


@posts.route('/basket')
@admin_only
def basket():
    posts = Post.get(is_active=False)
    for post in posts:
        post.body = support.first_paragraph(post.body)
    return render_template('draft.html', posts=posts)
