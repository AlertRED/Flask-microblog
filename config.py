class Config(object):
    SECRET_KEY = 'qwertyuiopqwertyuiopqwertyuiopqwertyuiopww'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_HEIGHT = 100
    CKEDITOR_LANGUAGE = 'ru'
    # CKEDITOR_PKG_TYPE = 'basic'
    CKEDITOR_ENABLE_CODESNIPPET = True
    USER_EMAIL_SENDER_EMAIL = 'drammtv@gmail.com'
    USER_UNAUTHENTICATED_ENDPOINT = 'login'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@127.0.0.1/microblog'
    ENV = 'DevelopmentConfig'
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgres://dwetqmnbbarnpg:201161c755cbab58edc7e671d1d9f9273e6f6ea2997c3684582299e71f0b6f8a@ec2-174-129-18-98.compute-1.amazonaws.com:5432/ddd1jtv2tt3601"
    ENV = 'ProductionConfig'
    DEBUG = False
    TESTING = False