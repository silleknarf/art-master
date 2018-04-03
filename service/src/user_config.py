#/usr/bin/python

from public_config import DevelopmentConfig, ProductionConfig

class UserDevelopmentConfig(DevelopmentConfig):
    # Set you details for your local
    # database configuration
    DATABASE_USERNAME = ""
    DATABASE_PASSWORD = ""
    DATABASE_NAME = "art-master-dev"

class PrivateProductionConfig(ProductionConfig):
    DATABASE_USERNAME = ""
    DATABASE_PASSWORD = ""
    DATABASE_NAME = ""
