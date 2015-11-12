

class Config(object):
    SECRET_KEY = 'a90bd0b2640d62d434d35c51ba679f45e4cefb12a09cb10c'
    # DB_USER = 'azureuser'
    # DB_PASSWORD = 'T*eFfland93'
    DB_USER = 'henrique'
    DB_PASSWORD = '123'
    PHOTO_DIR = "cooking/static/photos/"

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    DATABASE = 'cooking_production'
    HOST = '0.0.0.0'
    PORT = 5000

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE = 'cooking_development'
    HOST = '0.0.0.0'
    PORT = 5000
