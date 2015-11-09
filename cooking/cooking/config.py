

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'a90bd0b2640d62d434d35c51ba679f45e4cefb12a09cb10c'
    DB_USER = 'azureuser'
    DB_PASSWORD = 'T*eFfland93'
    PHOTO_DIR = "cooking/static/photos/"

class ProductionConfig(Config):
    DEBUG = False
    DATABASE = 'cooking_production'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE = 'cooking_development'
    HOST='0.0.0.0'
    PORT =5000
