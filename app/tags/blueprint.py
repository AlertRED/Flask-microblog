from flask import render_template, Blueprint, redirect, url_for, flash, request

from app import support
from app.forms import TagForm
from app.models import Tag, Post
from app.support import admin_only

tags = Blueprint('tags', __name__, template_folder='templates')


@tags.route('/<slug>', methods=['GET'])
def tag_posts(slug):
    tag = Tag.get_first(slug=slug)
    posts = Post.get(tags=[tag], is_active=True)
    for post in posts:
        post.body = support.first_paragraph(post.body)
    return render_template('all_posts.html', posts=posts)


@tags.route('/<slug>/edit', methods=['GET', 'POST'])
@admin_only
def edit_tag(slug):
    if request.method == 'POST':
        name, color = request.form['name'], request.form['color']
        tag = Tag.get_first(slug=slug)
        if tag:
            try:
                tag.update(name=name, color=color)
            except Exception as e:
                flash(str(e), 'alert')
            else:
                flash('Тег обновлен', 'success')
        return redirect(url_for("tags.all_tags"))
    tags = Tag.get()
    form = TagForm()
    tag = Tag.get_first(slug=slug)
    if tag:
        form.name.data = tag.name
        form.color.data = tag.color
    return render_template('tags.html', tags=tags, form=form, button='Изменить')


@tags.route('/', methods=['GET', 'POST'])
@admin_only
def all_tags():
    if request.method == 'POST':
        name, color = request.form['name'], request.form['color']
        try:
            Tag.create(name=name, color=color)
        except Exception as e:
            flash(str(e), 'alert')
        else:
            flash('Тег создан', 'success')
        return redirect(url_for("tags.all_tags"))
    tags = Tag.get()
    form = TagForm()
    return render_template('tags.html', tags=tags, form=form, button='Создать')


@tags.route('/<slug>/delete', methods=['GET'])
@admin_only
def delete(slug):
    tag = Tag.get_first(slug=slug)
    if tag:
        tag.delete()
        flash('Тег удален', 'success')
    else:
        flash('Тег не найден', 'alert')
    return redirect(url_for("tags.all_tags"))


@tags.route('/<slug>/destroy', methods=['GET'])
@admin_only
def destroy(slug):
    tag = Tag.get_first(slug=slug)
    if tag:
        tag.destroy()
        flash('Тег удален навсегда', 'success')
    else:
        flash('Тег не найден', 'alert')
    return redirect(url_for("tags.all_tags"))


@tags.route('/<slug>/restore', methods=['GET'])
@admin_only
def restore(slug):
    tag = Tag.get_first(slug=slug)
    if tag:
        tag.update(is_active=True)
        flash('Тег восстановлен', 'success')
    else:
        flash('Тег не найден', 'alert')
    return redirect(url_for("tags.all_tags"))