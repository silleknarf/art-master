# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Entry(Base):
    __tablename__ = 'Entry'

    EntryId = Column(INTEGER(11), primary_key=True)
    RoomId = Column(ForeignKey('Room.RoomId'), nullable=False, index=True)
    UserId = Column(ForeignKey('User.UserId'), nullable=False, index=True)
    RoundId = Column(ForeignKey('Round.RoundId'), index=True)
    MinigameId = Column(ForeignKey('Minigame.MinigameId'), nullable=False, index=True, server_default=text("'1'"))

    Minigame = relationship('Minigame')
    Room = relationship('Room')
    Round = relationship('Round', primaryjoin='Entry.RoundId == Round.RoundId')
    User = relationship('User')


class Minigame(Base):
    __tablename__ = 'Minigame'

    MinigameId = Column(INTEGER(11), primary_key=True)
    Name = Column(String(40), nullable=False)


class Round(Base):
    __tablename__ = 'Round'

    RoundId = Column(INTEGER(11), primary_key=True)
    RoomId = Column(ForeignKey('Room.RoomId'), nullable=False, index=True)
    StageStateId = Column(INTEGER(11))
    StageStateStartTime = Column(DateTime)
    StageStateEndTime = Column(DateTime)
    EntryId = Column(ForeignKey('Entry.EntryId'), index=True)

    Entry = relationship('Entry', primaryjoin='Round.EntryId == Entry.EntryId')
    Room = relationship('Room')


class StageState(Base):
    __tablename__ = 'StageState'

    StageStateId = Column(INTEGER(11), primary_key=True)
    StageStateName = Column(String(20), nullable=False)


class User(Base):
    __tablename__ = 'User'

    UserId = Column(INTEGER(11), primary_key=True)
    Username = Column(String(40), nullable=False)
    Score = Column(INTEGER(11), server_default=text("'0'"))


class EntryComponent(Base):
    __tablename__ = 'EntryComponent'
    __table_args__ = (
        Index('UC_EntryComponent', 'EntryId', 'Key', unique=True),
    )

    EntryComponentId = Column(INTEGER(11), primary_key=True)
    EntryId = Column(ForeignKey('Entry.EntryId', ondelete='CASCADE'), nullable=False)
    Key = Column(String(500), nullable=False, server_default=text("''"))
    Value = Column(String(500), nullable=False, server_default=text("''"))

    Entry = relationship('Entry')


class Image(Base):
    __tablename__ = 'Image'
    __table_args__ = (
        Index('UC_Image', 'UserId', 'RoundId', unique=True),
    )

    ImageId = Column(INTEGER(11), primary_key=True)
    UserId = Column(INTEGER(11), nullable=False)
    RoundId = Column(ForeignKey('Round.RoundId'), nullable=False, index=True)
    ImageBase64 = Column(Text, nullable=False)

    Round = relationship('Round')


class Room(Base):
    __tablename__ = 'Room'

    RoomId = Column(INTEGER(11), primary_key=True)
    RoomCode = Column(String(4))
    OwnerUserId = Column(ForeignKey('User.UserId'), index=True)
    CurrentRoundId = Column(INTEGER(11))
    MinigameId = Column(ForeignKey('Minigame.MinigameId'), nullable=False, index=True, server_default=text("'1'"))

    Minigame = relationship('Minigame')
    User = relationship('User')


class Rating(Base):
    __tablename__ = 'Rating'

    RatingId = Column(INTEGER(11), primary_key=True)
    RaterUserId = Column(ForeignKey('User.UserId'), nullable=False, index=True)
    ImageId = Column(ForeignKey('Image.ImageId'), index=True)
    Rating = Column(INTEGER(11), nullable=False)
    RoundId = Column(ForeignKey('Round.RoundId'), index=True)
    EntryId = Column(ForeignKey('Entry.EntryId'), index=True)

    Entry = relationship('Entry')
    Image = relationship('Image')
    User = relationship('User')
    Round = relationship('Round')


class RoomUser(Base):
    __tablename__ = 'RoomUser'
    __table_args__ = (
        Index('RoomId', 'RoomId', 'UserId', unique=True),
    )

    RoomUserId = Column(INTEGER(11), primary_key=True)
    RoomId = Column(ForeignKey('Room.RoomId'), nullable=False)
    UserId = Column(ForeignKey('User.UserId'), nullable=False, index=True)

    Room = relationship('Room')
    User = relationship('User')
