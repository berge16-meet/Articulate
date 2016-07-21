import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__='user'
	firstname=Column(String(64))
	lastname=Column(String(64))
	email=Column(String(64))
	username=Column(String(64), primary_key=True)
	password=Column(String(64))
	interests=Column(String(64))
	nationality=Column(String(64))
	gender=Column#it's a radio, so what type should it be?
	dob=Column(String(64))
	mob=Column(String(64))
	yob=Column#checkout type!
	bio=Column(String(250))
	pic=Column(String(250))

'''class Gallery(Base):
	__tablename__='gallery'	
	pic=Column(String(250))
'''
