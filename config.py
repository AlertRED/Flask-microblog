class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@127.0.0.1/microblog'
    SECRET_KEY = 'qwertyuiopqwertyuiopqwertyuiopqwertyuiopww'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_HEIGHT = 100
    CKEDITOR_ENABLE_CODESNIPPET = True
    USER_EMAIL_SENDER_EMAIL = 'drammtv@gmail.com'
    USER_UNAUTHENTICATED_ENDPOINT = 'login'


class DevelopmentConfig(Config):
    ENV = 'DevelopmentConfig'
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    ENV = 'ProductionConfig'
    DEBUG = False
    TESTING = False
