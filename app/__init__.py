from flask import Flask
from config import DevelopmentConfig, ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config.from_object(ProductionConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
ckeditor = CKEditor(app)

from app import routes, models
from app.posts.blueprint import posts
from app.tags.blueprint import tags

### Blueprints ###
app.register_blueprint(posts, url_prefix='/blog')
app.register_blueprint(tags, url_prefix='/tags')
