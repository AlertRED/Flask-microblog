from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
ckeditor = CKEditor(app)

### Blueprints ###
from app import routes, models
from app.posts.blueprint import posts
app.register_blueprint(posts, url_prefix='/blog')

