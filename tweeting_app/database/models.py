from sqlalchemy import Boolean, Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique = True,index = True)
    email = Column(String,unique = True, index = True)
    password = Column(String)
    is_active = Column(Boolean,default = False)
    is_superuser = Column(Boolean,default = False)
    time_created = Column(DateTime,default = datetime.utcnow)

    tweet = relationship("Tweet",back_populates="owner")


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(Integer,primary_key=True,index=True)
    data = Column(String)
    time_created = Column(DateTime,default=datetime.utcnow)
    last_modified = Column(DateTime,default=datetime.utcnow)
    user_id = Column(Integer,ForeignKey("user.id"))

    owner = relationship("User",back_populates="tweet")