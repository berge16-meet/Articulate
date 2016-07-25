import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	firstname = Column(String(64))
	lastname = Column(String(64))
	email = Column(String(64))
	username = Column(String(64))
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
	comments = Column(String(300))