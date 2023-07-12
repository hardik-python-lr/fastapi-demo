from database import Base
from sqlalchemy import Column, Integer, DateTime, String, Boolean
from datetime import datetime


class User(Base):
    """
    Represents a user in the system.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    phn_no = Column(Integer)
    password = Column(String)
    is_active = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
