from flask_login import current_user, login_required
from functools import wraps
from flask import flash, redirect, url_for


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


def first_paragraph(body):
    return body[:body.find('\n')] or body
