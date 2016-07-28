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
	photos = relationship('Gallery', backref = 'User', lazy = 'dynamic')

topic_gallery_association_table = Table('association', Base.metadata, Column('topic_id', Integer, ForeignKey('topic.id')), Column('gallery_id', Integer, ForeignKey('gallery.id')))

class Topic(Base):
	__tablename__ = 'topic'
	id = Column(Integer, primary_key=True)
	topic = Column(String(64), unique=True)
	posts = relationship("Gallery", secondary = topic_gallery_association_table, back_populates="topics")

class Gallery(Base):
	__tablename__ = 'gallery'
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('user.id'))
	photo = Column(String(255))
	description = Column(String(140))
	likes = Column(Integer)
	topics = relationship("Topics", secondary = topic_gallery_association_table,  back_populates="galleries")
	comments = relationship('Comment', backref='Gallery')

class Comment(Base):
	__tablename__='comments'
	id = Column(Integer,primary_key=True)
	gallery_id = Column(Integer, ForeignKey('gallery.id'))
	parent_id = Column(Integer, ForeignKey('comment.id'))
	user_id = Column(Integer)
	text = Column(String(400))
	time=Column(Time)
	sub_comments = relationship('Comment', backref='Comment')


#def foo(comments):
#	output = []
#	for comment in comments:
#		output.append(comment)
#		for sub_comment in comment.sub_comments:
#			output += foo(sub_comment)
#		return output
