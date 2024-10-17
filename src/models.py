import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    bio = Column(String(500))
    profile_picture = Column(String(500))

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    followers = relationship("Follow", back_populates="follower", foreign_keys='Follow.follower_id')
    followings = relationship("Follow", back_populates="followed", foreign_keys='Follow.followed_id')
    sent_messages = relationship("DirectMessage", back_populates="sender")
    received_messages = relationship("DirectMessage", back_populates="receiver")

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    likes = Column(Integer, default=0)
    location = Column(String(250))

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    tags = relationship("Tag", back_populates="post")

class Comment(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Follow(Base):
    __tablename__ = 'follow'
    
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'))
    followed_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    follower = relationship("User", back_populates="followers", foreign_keys=[follower_id])
    followed = relationship("User", back_populates="followings", foreign_keys=[followed_id])

class DirectMessage(Base):
    __tablename__ = 'direct_message'
    
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.id'))
    receiver_id = Column(Integer, ForeignKey('user.id'))
    content = Column(String(500), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="received_messages", foreign_keys=[receiver_id])

class Tag(Base):
    __tablename__ = 'tag'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="tags")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
