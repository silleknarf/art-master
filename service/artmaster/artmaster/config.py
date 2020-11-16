import os

class Config(object):
    DEBUG = os.getenv("CRAICBOX_DEBUG")=="1"
    TESTING = False
    HOST = os.getenv("CRAICBOX_HOST")
    URL = os.getenv("CRAICBOX_URL")
    DATABASE_SERVER = "db:3306"
    DATABASE_USERNAME = "root"
    DATABASE_NAME = "craicbox"
    DATABASE_PASSWORD = os.getenv("CRAICBOX_DATABASE_PASSWORD")
    SOCKETIO_PASSWORD = os.getenv("SOCKETIO_PASSWORD")
