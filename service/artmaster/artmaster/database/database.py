#!/usr/bin/python

import logging
import sys
sys.path.append("..")

from .data_model import *
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

connection_string = ('mysql://%s:%s@%s/%s' %
    (Config.DATABASE_USERNAME,
    Config.DATABASE_PASSWORD,
    Config.DATABASE_SERVER,
    Config.DATABASE_NAME))

sql_alchemy_logger = logging.getLogger('sqlalchemy.engine')
sql_alchemy_handler = logging.FileHandler("craicbox.sql.log")
sql_alchemy_logger.handlers = []
sql_alchemy_logger.addHandler(sql_alchemy_handler)
sql_alchemy_logger.setLevel(logging.INFO)

engine = create_engine(
    connection_string,
    encoding="utf8",
    echo=False,
    isolation_level="READ_COMMITTED")

session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))
