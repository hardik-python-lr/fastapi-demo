from database import Base
from sqlalchemy import Column, Integer, DateTime, String, Boolean
from datetime import datetime


class Product(Base):
    """
    Represents a product in the inventory.
    """

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String, unique=True)
    price = Column(Integer)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
