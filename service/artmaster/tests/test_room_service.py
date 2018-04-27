#!/usr/bin/python

import unittest
import mock
import sqlite3
import sys
sys.path.append("../artmaster")
from artmaster.services import room_service
from artmaster import app
from artmaster.database.data_model import *
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from sqlalchemy.engine import Engine

# Turn on foreign key constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:  # play well with other DB backends
       cursor = dbapi_connection.cursor()
       cursor.execute("PRAGMA foreign_keys=ON")
       cursor.close()

class TestRoomService(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.engine = create_engine('sqlite://',
                    connect_args={'check_same_thread':False},
                    poolclass=StaticPool)
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
    
    @mock.patch('artmaster.services.room_service.jsonify')
    def test_add_user_to_room(self, jsonify):
        room_service.session = self.session
        room_service.session.add(User(UserId=1, Username="Test"))
        room_service.session.add(Room(RoomId=1, OwnerUserId=1))
        room_service.session.commit()
        room_id = 1
        user_id = 1
        room_service.add_user_to_room(room_id, user_id) 
        room_user_entity = self.session.query(RoomUser).first()
        self.assertEqual(room_user_entity.RoomId, 1)
        self.assertEqual(room_user_entity.UserId, 1)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoomService)
    suite.debug()

