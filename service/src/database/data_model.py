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
    Location = Column(String(255), nullable=False)


class Rating(Base):
    __tablename__ = 'Rating'

    RatingId = Column(Integer, primary_key=True)
    RaterUserId = Column(ForeignKey(u'User.UserId'), nullable=False, index=True)
    RoundImageId = Column(ForeignKey(u'RoundImage.RoundImageId'), nullable=False, index=True)
    Rating = Column(Integer, nullable=False)

    User = relationship(u'User')
    RoundImage = relationship(u'RoundImage')


class Room(Base):
    __tablename__ = 'Room'

    RoomId = Column(Integer, primary_key=True)
    RoomCode = Column(String(4))
    CurrentRoundId = Column(Integer)

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
    RoomId = Column(ForeignKey(u'Room.RoomId'), nullable=False)
    StageStateId = Column(Integer, nullable=True)
    StageStateStartTime = Column(DateTime, nullable=False)
    StageStateEndTime = Column(DateTime, nullable=False)
    
    Room = relationship(u'Room')
    
class StageState(Base):
    __tablename__ = 'StageState'
    
    StageStateId = Column(Integer, primary_key=True, autoincrement=False)
    StageStateName = Column(String(20), nullable=False)

class RoundImage(Base):
    __tablename__ = 'RoundImage'

    RoundImageId = Column(Integer, primary_key=True)
    RoundId = Column(ForeignKey(u'Round.RoundId'), nullable=False, index=True)
    ImageId = Column(ForeignKey(u'Image.ImageId'), nullable=False, index=True)

    Image = relationship(u'Image')
    Round = relationship(u'Round')


class User(Base):
    __tablename__ = 'User'

    UserId = Column(Integer, primary_key=True)
    Username = Column(String(40), nullable=False)