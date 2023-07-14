from database import Base
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from datetime import datetime
from enum import Enum


class TaskCategory(str, Enum):
    """
    Represents the category of a task.

    Inherits from the `str` class and the `Enum` class.
    """

    ADMINISTRATIVE = "administrative"
    CREATIVE = "creative"
    RESEARCH = "research"
    TECHNICAL = "technical"


class Task(Base):
    """
    Represents a task in the database.
    """

    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String)
    assign_to = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
