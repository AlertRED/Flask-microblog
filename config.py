import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_HEIGHT = 100
    CKEDITOR_LANGUAGE = 'ru'
    # CKEDITOR_PKG_TYPE = 'basic'
    CKEDITOR_ENABLE_CODESNIPPET = True
    USER_EMAIL_SENDER_EMAIL = 'drammtv@gmail.com'
    USER_UNAUTHENTICATED_ENDPOINT = 'login'
    SECRET_KEY = config.get('ACCESSES', 'SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('ACCESSES', 'DATABASE_URI')


class DevelopmentConfig(Config):
    ENV = 'DevelopmentConfig'
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    ENV = 'ProductionConfig'
    DEBUG = False
    TESTING = False