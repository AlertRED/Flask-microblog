import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_HEIGHT = 100
    CKEDITOR_LANGUAGE = 'ru'
    # CKEDITOR_PKG_TYPE = 'basic'
    CKEDITOR_ENABLE_CODESNIPPET = True
    USER_EMAIL_SENDER_EMAIL = 'drammtv@gmail.com'
    USER_UNAUTHENTICATED_ENDPOINT = 'login'



class DevelopmentConfig(Config):
    ENV = 'DevelopmentConfig'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'qwerty'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@127.0.0.1/microblog'


class ProductionConfig(Config):
    ENV = 'ProductionConfig'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
