from flask import render_template, Blueprint, request, flash, redirect, url_for
from app.models import Post, Tag
from app import db, support
from flask_login import current_user
from app.forms import PostForm


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if current_user.is_authenticated and current_user.username == 'ieaiaio':
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            timestamp = request.form['timestamp']
            try:
                post = Post(title=title, body=body, timestamp=timestamp)  # , tags=[tag]
                db.session.add(post)
                db.session.commit()
            except Exception as e:
                flash(str(e), 'alert')
            else:
                flash('Пост успешно выложен', 'success')
            return redirect(url_for('index'))
        form = PostForm()
        tags = Tag.query.all()
        return render_template('edit_post.html', form=form, tags=tags, title='Создание поста', button='Создать')
    return redirect(url_for('index'))


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('post_detail.html', post=post)


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if request.method == 'POST':
        form = PostForm(formdate=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for("posts.post_detail", slug=post.slug))
    form = PostForm(obj=post)
    return render_template('edit_post.html', post=post, form=form, title='Изменение поста', button='Сохранить')


@posts.route('/<slug>/restore/', methods=['POST', 'GET'])
def restore(slug):
    if request.method == 'POST':
        return redirect(url_for("index"))
    post = Post.query.filter(Post.slug == slug).first()
    post.is_active = True
    db.session.commit()
    flash('Пост восстановлен', 'success')
    return redirect(url_for("index"))


@posts.route('/<slug>/to_basket/', methods=['POST', 'GET'])
def to_basket(slug):
    if request.method == 'POST':
        return redirect(url_for("index"))
    post = Post.query.filter(Post.slug == slug).first()
    post.is_active = False
    db.session.commit()
    flash('Пост отправлен в корзину', 'success')
    return redirect(url_for("index"))


@posts.route('/<slug>/delete/', methods=['POST', 'GET'])
def delete(slug):
    if request.method == 'POST':
        return redirect(url_for("index"))
    post = Post.query.filter(Post.slug == slug).first()
    db.session.delete(post)
    db.session.commit()
    flash('Пост успешно удален', 'success')
    return redirect(url_for("index"))


@posts.route('/')
def all_posts():
    posts = Post.query.filter(Post.is_active).order_by(Post.timestamp.desc()).all()
    for post in posts:
        post.body = support.first_paragraph(post.body)
    return render_template('all_posts.html', posts=posts)


@posts.route('/basket')
def basket():
    posts = Post.query.filter(Post.is_active == False).order_by(Post.timestamp.desc()).all()
    for post in posts:
        post.body = support.first_paragraph(post.body)
    return render_template('draft.html', posts=posts)
