class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_NAME = "art-master"
    DATABASE_SERVER = "localhost"

class ProductionConfig(Config):
    DATABASE_USERNAME = "user"
    DATABASE_PASSWORD = "password"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True