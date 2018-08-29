from flask import render_template, Blueprint, request, flash, redirect, url_for
from app.models import Post
from app import app, db
from flask_login import current_user
from app.forms import PostForm

posts = Blueprint('posts', __name__, template_folder='templates')



def first_paragraph(body):
    return body[:body.find('\n')] or body

@posts.route('/create_post', methods=['POST', 'GET'])
def create_post():
    if current_user.is_authenticated and current_user.username =='ieaiaio':
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
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
        return render_template('edit_post.html', form=form, title='Создание поста', button='Создать')
    return redirect(url_for('index'))

@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('post.html', post=post)

@posts.route('/<slug>/edit/', methods=['POST','GET'])
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if request.method == 'POST':
        form = PostForm(formdate=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for("posts.post_detail",slug = post.slug))
    form = PostForm(obj = post)
    return render_template('edit_post.html', post = post, form = form, title='Изменение поста', button='Сохранить')

@posts.route('/')
def all_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    for post in posts:
    	post.body = first_paragraph(post.body)

    return render_template('all_posts.html', posts=posts)