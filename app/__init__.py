import os

from flask import Flask
from config import DevelopmentConfig, ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config.from_object(ProductionConfig)
print(os.environ)
# postgres://dwetqmnbbarnpg:201161c755cbab58edc7e671d1d9f9273e6f6ea2997c3684582299e71f0b6f8a@ec2-174-129-18-98.compute-1.amazonaws.com:5432/ddd1jtv2tt3601


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
