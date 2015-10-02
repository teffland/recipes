

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DB_USER = 'henrique'
    DB_PASSWORD = '123'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE = 'cooking_production'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE = 'cooking_development'
