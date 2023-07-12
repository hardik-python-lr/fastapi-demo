from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker

# Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency function to get a database session.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()
