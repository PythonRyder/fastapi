from sqlalchemy import TIMESTAMP, Column, ForeignKey,Integer, String,Boolean,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from traitlets import default
from sqlalchemy.orm import relationship
# from . database import Base

Base = declarative_base()  #all models will be of this base class

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean,server_default = "True", default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    owner_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"),nullable=False)

    #This will be property for our post so when we retrieve a posts
    # it is going to return a owner property whichfigure out the  relationaship 
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable=False, unique= True)
    password = Column(String, nullable=False)
    user_phone = Column(String, nullable=False )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    # user_phone = Column(String, nullable=False )

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete = "CASCADE"), primary_key = True )
    post_id = Column(Integer, ForeignKey("posts.post_id", ondelete = "CASCADE"), primary_key = True )






 