from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import re

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', str(s))


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )
        
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: username {}, id: {}>'.format(self.username, self.id)
        

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    slug = db.Column(db.String(100), unique=True)

    def __init__(self, *args,**kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.name)

    def __repr__(self):
        return 'Rag: name {}'.format(self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(65536))
    slug = db.Column(db.String(255), unique=True)

    is_active = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post: name {}, active {}>'.format(self.title,self.is_active)