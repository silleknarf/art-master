# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Image(Base):
    __tablename__ = 'Image'

    ImageId = Column(Integer, primary_key=True)
    UserId = Column(Integer, nullable=False)
    RoundId = Column(ForeignKey(u'Round.RoundId'), nullable=False, index=True)
    Location = Column(String(255), nullable=False)

    Round = relationship(u'Round')


class Rating(Base):
    __tablename__ = 'Rating'

    RatingId = Column(Integer, primary_key=True)
    RaterUserId = Column(ForeignKey(u'User.UserId'), nullable=False, index=True)
    ImageId = Column(ForeignKey(u'Image.ImageId'), nullable=False, index=True)
    Rating = Column(Integer, nullable=False)

    Image = relationship(u'Image')
    User = relationship(u'User')


class Room(Base):
    __tablename__ = 'Room'

    RoomId = Column(Integer, primary_key=True)
    RoomCode = Column(String(4))
    OwnerUserId = Column(ForeignKey(u'User.UserId'), nullable=False, index=True)
    CurrentRoundId = Column(Integer)

    User = relationship(u'User')


class RoomUser(Base):
    __tablename__ = 'RoomUser'
    __table_args__ = (
        Index('RoomId', 'RoomId', 'UserId', unique=True),
    )

    RoomUserId = Column(Integer, primary_key=True)
    RoomId = Column(ForeignKey(u'Room.RoomId'), nullable=False)
    UserId = Column(ForeignKey(u'User.UserId'), nullable=False, index=True)

    Room = relationship(u'Room')
    User = relationship(u'User')


class Round(Base):
    __tablename__ = 'Round'

    RoundId = Column(Integer, primary_key=True)
    RoomId = Column(ForeignKey(u'Room.RoomId'), nullable=False, index=True)
    StageStateId = Column(Integer)
    StageStateStartTime = Column(DateTime)
    StageStateEndTime = Column(DateTime)

    Room = relationship(u'Room')


class StageState(Base):
    __tablename__ = 'StageState'

    StageStateId = Column(Integer, primary_key=True)
    StageStateName = Column(String(20), nullable=False)


class User(Base):
    __tablename__ = 'User'

    UserId = Column(Integer, primary_key=True)
    Username = Column(String(40), nullable=False)


class Word(Base):
    __tablename__ = 'Word'

    WordId = Column(Integer, primary_key=True)
    RoomId = Column(ForeignKey(u'Room.RoomId'), nullable=False, index=True)
    UserId = Column(ForeignKey(u'User.UserId'), nullable=False, index=True)
    Word = Column(String(50), nullable=False)

    Room = relationship(u'Room')
    User = relationship(u'User')