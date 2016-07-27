import os
import sys
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	firstname = Column(String(64))
	lastname = Column(String(64))
	email = Column(String(64),unique=True)
	username = Column(String(64),unique=True)
	password = Column(String(64))
	nationality = Column(String(64))
	gender = Column(String(20))
	date = Column(String(64))
	bio = Column(String(250))
	profilepic = Column(String(250))

class Gallery(Base):
	__tablename__ = 'gallery'
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer)
	photo = Column(String(250))
	description = Column(String(140))
	likes = Column(Integer)
	comments = relationship('Comment', backref='Gallery', lazy='dynamic')

class Comment(Base):
	__tablename__='comments'
	id = Column(Integer,primary_key=True)
	gallery_id = Column(Integer, ForeignKey('gallery.id'))
	user_id = Column(Integer)
	text = Column(String(100))
	time=Column(Time)


