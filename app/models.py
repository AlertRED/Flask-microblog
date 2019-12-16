from datetime import datetime

from sqlalchemy.orm import relationship

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

user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                     )

role_rule = db.Table('role_rule',
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                     db.Column('rule_id', db.Integer, db.ForeignKey('rule.id'))
                     )


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    __SKIP = object()
    roles = relationship("Role", secondary=role_rule, back_populates="rules")

    def __init__(self, *args, **kwargs):
        super(Rule, self).__init__(*args, **kwargs)

    def add_role(self, *args):
        self.roles += args
        db.session.commit()
        return self

    @staticmethod
    def create(name):
        if Rule.get_first(name):
            raise Exception('Правило уже существует')
        rule = Rule(name=name)
        db.session.add(rule)
        db.session.commit()
        return rule

    @staticmethod
    def get(name=__SKIP) -> list:
        filters = dict()
        if name != Rule.__SKIP:
            filters['name'] = name
        return Rule.query.filter_by(**filters).all()

    @staticmethod
    def get_first(name=__SKIP):
        filters = dict()
        if name != Rule.__SKIP:
            filters['name'] = name
        return Rule.query.filter_by(**filters).first()

    def update(self, name=__SKIP):
        if name != Rule.__SKIP:
            self.name = name
        db.session.commit()
        return self

    def delete(self):
        self.is_active = False
        db.session.commit()
        return self

    def destroy(self):
        db.session.delete(self)
        db.session.commit()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    __SKIP = object()

    rules = relationship("Rule", secondary=role_rule, back_populates="roles")
    users = relationship("User", secondary=user_role, back_populates="roles")

    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)

    def add_rule(self, *args):
        self.rules += args
        db.session.commit()
        return self

    @staticmethod
    def create(name):
        if Role.get_first(name):
            raise Exception('Роль уже существует')
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()
        return role

    @staticmethod
    def get(name=__SKIP) -> list:
        filters = dict()
        if name != Role.__SKIP:
            filters['name'] = name
        return Role.query.filter_by(**filters).all()

    @staticmethod
    def get_first(name=__SKIP):
        filters = dict()
        if name != Role.__SKIP:
            filters['name'] = name
        return Role.query.filter_by(**filters).first()

    def update(self, name=__SKIP):
        if name != Role.__SKIP:
            self.name = name
        db.session.commit()
        return self

    def delete(self):
        self.is_active = False
        db.session.commit()
        return self

    def destroy(self):
        db.session.delete(self)
        db.session.commit()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    __SKIP = object()

    roles = relationship("Role", secondary=user_role, back_populates="users")

    def add_role(self, *args):
        User.roles += args
        db.session.commit()
        return self

    def __set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__set_password(kwargs['password_hash'])

    @staticmethod
    def create(username, password):
        if User.get_first(username):
            raise Exception('Пользователь уже существует')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get(username=__SKIP, is_active=__SKIP) -> list:
        filters = dict()
        if username != User.__SKIP:
            filters['username'] = username
        if is_active != User.__SKIP:
            filters['is_active'] = is_active
        return User.query.filter_by(**filters).all()

    @staticmethod
    def get_first(username=__SKIP, is_active=__SKIP):
        filters = dict()
        if username != User.__SKIP:
            filters['username'] = username
        if is_active != User.__SKIP:
            filters['is_active'] = is_active
        return User.query.filter_by(**filters).first()

    def update(self, username=__SKIP):
        if username != User.__SKIP:
            self.username = username
        db.session.commit()
        return self

    def delete(self):
        self.is_active = False
        db.session.commit()
        return self

    def destroy(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<User: username {}, id: {}>'.format(self.username, self.id)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    color = db.Column(db.String(8))
    __SKIP = object()

    posts = relationship("Post", secondary=post_tags, back_populates="tags")


    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.generate_slug()

    @staticmethod
    def create(name, timestamp):
        if Tag.get_first(name=name):
            raise Exception("Тег уже существует")
        tag = Tag(name, timestamp)
        db.session.add(tag)
        db.session.commit()
        return tag

    @staticmethod
    def get(name=__SKIP, slug=__SKIP, is_active=__SKIP, timestamp=__SKIP) -> list:
        filters = dict()
        if name != Tag.__SKIP:
            filters['name'] = name
        if slug != Tag.__SKIP:
            filters['slug'] = slug
        if is_active != Tag.__SKIP:
            filters['is_active'] = is_active
        if timestamp != Tag.__SKIP:
            filters['timestamp'] = timestamp
        return Tag.query.filter_by(**filters).order_by(Tag.timestamp.desc()).all()

    @staticmethod
    def get_first(name=__SKIP, body=__SKIP, slug=__SKIP, is_active=__SKIP, timestamp=__SKIP):
        filters = dict()
        if name != Tag.__SKIP:
            filters['name'] = name
        if body != Tag.__SKIP:
            filters['body'] = body
        if slug != Tag.__SKIP:
            filters['slug'] = slug
        if is_active != Tag.__SKIP:
            filters['is_active'] = is_active
        if timestamp != Tag.__SKIP:
            filters['timestamp'] = timestamp
        return Tag.query.filter_by(**filters).first_or_404()

    def update(self, name=__SKIP, slug=__SKIP, is_active=__SKIP, timestamp=__SKIP):
        if name != Tag.__SKIP:
            self.name = name
        if slug != Tag.__SKIP:
            self.slug = slug
        if is_active != Tag.__SKIP:
            self.is_active = is_active
        if timestamp != Tag.__SKIP:
            self.timestamp = timestamp
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        self.is_active = False
        db.session.add(self)
        db.session.commit()
        return self

    def destroy(self):
        self.is_active = False
        db.session.delete(self)
        db.session.commit()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return 'Tag: name {}'.format(self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(65536))
    slug = db.Column(db.String(255), unique=True)
    __SKIP = object()

    is_active = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    @staticmethod
    def create(title, body, timestamp):
        if Post.get_first(title=title):
            raise Exception("Пост с таким названием уже существует")
        post = Post(title, body, timestamp)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def get_first(title=__SKIP, body=__SKIP, slug=__SKIP, is_active=__SKIP, timestamp=__SKIP):
        filters = dict()
        if title != Post.__SKIP:
            filters['title'] = title
        if body != Post.__SKIP:
            filters['body'] = body
        if slug != Post.__SKIP:
            filters['slug'] = slug
        if is_active != Post.__SKIP:
            filters['is_active'] = is_active
        if timestamp != Post.__SKIP:
            filters['timestamp'] = timestamp
        return Post.query.filter_by(**filters).first_or_404()

    @staticmethod
    def get(title=__SKIP, body=__SKIP, slug=__SKIP, is_active=__SKIP, timestamp=__SKIP, limit=None) -> list:
        filters = dict()
        if title != Post.__SKIP:
            filters['title'] = title
        if body != Post.__SKIP:
            filters['body'] = body
        if slug != Post.__SKIP:
            filters['slug'] = slug
        if is_active != Post.__SKIP:
            filters['is_active'] = is_active
        if timestamp != Post.__SKIP:
            filters['timestamp'] = timestamp
        return Post.query.filter_by(**filters).order_by(Post.timestamp.desc()).limit(limit).all()

    def update(self, title=__SKIP, body=__SKIP, slug=__SKIP, is_active=__SKIP, timestamp=__SKIP):
        if title != Post.__SKIP:
            self.title = title
        if body != Post.__SKIP:
            self.body = body
        if slug != Post.__SKIP:
            self.slug = slug
        if is_active != Post.__SKIP:
            self.is_active = is_active
        if timestamp != Post.__SKIP:
            self.timestamp = timestamp
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        self.is_active = False
        db.session.add(self)
        db.session.commit()
        return self

    def destroy(self):
        self.is_active = False
        db.session.delete(self)
        db.session.commit()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post: name {}, active {}>'.format(self.title, self.is_active)
