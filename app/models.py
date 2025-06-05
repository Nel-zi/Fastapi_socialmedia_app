# Models represent each of the tables in our database.
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
# from sqlalchemy.sql.expression import text
from .database import Base

# The table for all post created on the social media webapp
class Post(Base):
    __tablename__ = "post"

    post_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)      # "users" in "users.user_id" is coming from the table name called "users" in the User class model
    user = relationship("User")
    summary = Column(String, nullable=True)


# The table for all the user account info
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



# The table for all the user likes info
class Likes(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("post.post_id", ondelete="CASCADE"), primary_key=True)
