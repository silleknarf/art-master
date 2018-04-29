#!/usr/bin/python

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from data_model import *
from user_config import UserDevelopmentConfig
from contextlib import contextmanager
import logging

config = UserDevelopmentConfig

connection_string = ('mysql://%s:%s@%s/%s' % 
    (config.DATABASE_USERNAME, 
    config.DATABASE_PASSWORD,
    config.DATABASE_SERVER,
    config.DATABASE_NAME))

logger = logging.getLogger('sqlalchemy.engine')
handler = logging.FileHandler("art-master.sql.log")        
handler.setLevel(logging.INFO)
logger.addHandler(handler)

logger = logging.getLogger('sqlalchemy.pool')
handler = logging.FileHandler("art-master.sql.log")        
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

engine = create_engine(
    connection_string,
    encoding="utf8", 
    echo=False)

print "test"

session_maker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

