# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String
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


class RoomUser(Base):
    __tablename__ = 'RoomUser'

    RoomUserId = Column(Integer, primary_key=True)
    RoomId = Column(ForeignKey(u'Room.RoomId'), nullable=False, index=True)
    UserId = Column(ForeignKey(u'User.UserId'), nullable=False, index=True)

    Room = relationship(u'Room')
    User = relationship(u'User')


class Round(Base):
    __tablename__ = 'Round'

    RoundId = Column(Integer, primary_key=True)


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
