#!/usr/bin/python

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from data_model import *
from user_config import UserDevelopmentConfig
from contextlib import contextmanager

config = UserDevelopmentConfig

connection_string = ('mysql://%s:%s@%s/%s' % 
    (config.DATABASE_USERNAME, 
    config.DATABASE_PASSWORD,
    config.DATABASE_SERVER,
    config.DATABASE_NAME))

engine = create_engine(
    connection_string,
    encoding="utf8", 
    echo=True)

session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))

