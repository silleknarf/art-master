import os

class Config(object):
    DEBUG = os.getenv("CRAICBOX_DEBUG")=="1"
    TESTING = False
    DATABASE_SERVER = "db:3306"
    DATABASE_USERNAME = "root"
    DATABASE_PASSWORD = os.getenv("CRAICBOX_DATABASE_PASSWORD")
    DATABASE_NAME = "art-master-dev"
    HOST = os.getenv("CRAICBOX_HOST")
