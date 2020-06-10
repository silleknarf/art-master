#!/usr/bin/python

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from data_model import *
import sys
sys.path.append("..")
from user_config import UserDevelopmentConfig, PrivateProductionConfig

class DatabaseBuilder():
    _config = None

    def __init__(self, config):
        self._config = config

    def build_database(self):
        self._create_database()
        self._populate_database_schema()

    def rebuild_database(self):
        # Let's not drop the db in PROD, just to be safe :)
        self._drop_database()
        self._create_database()
        self._populate_database_schema()

    def _get_engine(self, database=""):
        connection_string = ('mysql://%s:%s@%s/%s' % 
            (self._config.DATABASE_USERNAME, 
            self._config.DATABASE_PASSWORD,
            self._config.DATABASE_SERVER,
            database))
        engine = create_engine(
            connection_string,
            encoding="utf8", 
            echo=True)
        return engine

    def _create_database(self):
        engine = self._get_engine()
        conn = engine.connect()
        # Do not substitute user-supplied database names here.
        conn.execute("CREATE DATABASE `%s`" % self._config.DATABASE_NAME)
        conn.execute("COMMIT")
        conn.close()

    def _populate_database_schema(self):
        # Get a new engine for the just-created database and create a table.
        engine = self._get_engine(self._config.DATABASE_NAME)
        conn = engine.connect()
        Base.metadata.create_all(engine)
        conn.execute("COMMIT")
        conn.close()

        session = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine))

        session.add(Minigame(MinigameId=1, Name="Art Master"))
        session.add(Transition(MinigameId=1, StateTo=0))
        session.add(Transition(MinigameId=1, StateFrom=0, StateTo=2))
        session.add(Transition(MinigameId=1, StateFrom=2, StateTo=3))
        session.add(Transition(MinigameId=1, StateFrom=3, StateTo=4))

        session.add(Minigame(MinigameId=2, Name="Sentenced To Death"))
        session.add(Transition(MinigameId=2, StateTo=1))
        session.add(Transition(MinigameId=2, StateFrom=1, StateTo=2))
        session.add(Transition(MinigameId=2, StateFrom=2, StateTo=3))
        session.add(Transition(MinigameId=2, StateFrom=3, StateTo=4))
        session.commit()
        session.close()

    def _drop_database(self):
        engine = self._get_engine()
        conn = engine.connect()
        conn.execute("DROP DATABASE IF EXISTS `%s`" % self._config.DATABASE_NAME)
        conn.execute("COMMIT")
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage = (
            "Usage: ./create_database.py ARGS\n"
            "--dev\tcreate dev database\n"
            "--prod\tcreate prod database")
        print(usage)
    elif sys.argv[1] == "--prod":
        db_builder = DatabaseBuilder(PrivateProductionConfig)
        db_builder.build_database()
    elif sys.argv[1] == "--dev":
        db_builder = DatabaseBuilder(UserDevelopmentConfig)
        db_builder.rebuild_database()
    else:
        print("Invalid arguments")
