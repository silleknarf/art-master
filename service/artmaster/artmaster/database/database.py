#!/usr/bin/python

import logging
import sys
sys.path.append("..")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
from data_model import *
from config import Config

connection_string = ('mysql://%s:%s@%s/%s' %
    (Config.DATABASE_USERNAME,
    Config.DATABASE_PASSWORD,
    Config.DATABASE_SERVER,
    Config.DATABASE_NAME))

logger = logging.getLogger('sqlalchemy.engine')
handler = logging.FileHandler("art-master.sql.log")
logger.handlers = []
logger.addHandler(handler)
logger.setLevel(logging.INFO)

#logger = logging.getLogger('sqlalchemy.pool')
#handler = logging.FileHandler("art-master.sql.log")
#logger.handlers = []
#logger.addHandler(handler)
#logger.setLevel(logging.DEBUG)

engine = create_engine(
    connection_string,
    encoding="utf8",
    echo=False)

session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))

