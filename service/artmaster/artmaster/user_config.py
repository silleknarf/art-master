#/usr/bin/python

import os
from public_config import DevelopmentConfig, ProductionConfig

class UserDevelopmentConfig(DevelopmentConfig):
    # Set you details for your local
    # database configuration
    DATABASE_USERNAME = "root"
    DATABASE_PASSWORD = os.getenv("CRAICBOX_DATABASE_PASSWORD")
    DATABASE_NAME = "art-master-dev"

class PrivateProductionConfig(ProductionConfig):
    DATABASE_USERNAME = ""
    DATABASE_PASSWORD = os.getenv("CRAICBOX_DATABASE_PASSWORD")
    DATABASE_NAME = ""
