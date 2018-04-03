#!/usr/bin/python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_model import *
from user_config import UserDevelopmentConfig

config = UserDevelopmentConfig


class Database():
    _connection_string = ('mysql://%s:%s@%s/%s' % 
        (config.DATABASE_USERNAME, 
        config.DATABASE_PASSWORD,
        config.DATABASE_SERVER,
        config.DATABASE_NAME))

    def get_session(self):
        engine = create_engine(
            self._connection_string,
            encoding="utf8", 
            echo=True)

        art_master_session_maker = sessionmaker(bind=engine)
        return art_master_session_maker()

    @staticmethod
    def row_to_list(row):
        return [(col, getattr(row, col)) for col in row.__table__.columns.keys()]

def main():
    art_master_session = Database().get_session()
    first_symbol = art_master_session.query(User).first()
    print Database.row_to_list(first_symbol)

if __name__ == "__main__":
    main()

