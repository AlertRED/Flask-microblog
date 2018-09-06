from app import app, models

### ADMIN ###

from app.models import *
from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView
from flask_login import current_user


class AdminMixin():
	def is_accessible(self):
		return current_user.is_authenticated and current_user.username == 'ieaiaio'

class AdminView(AdminMixin, ModelView):
    pass

admin = Admin(app)
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))

### Blueprints ###

from app import routes, models
from app.posts.blueprint import posts
app.register_blueprint(posts, url_prefix='/blog')