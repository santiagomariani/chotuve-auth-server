import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class TestConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = "DEBUG"
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "WARN"

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig
}