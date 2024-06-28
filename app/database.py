from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Ensure this loads the .env file
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Function to get a database session.

    Returns:
        db (SessionLocal): A database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Image(Base):
    """
    SQLAlchemy model for the 'images' table.

    Attributes:
        id (int): The primary key of the image.
        depth (int): The depth of the image.
        path (str): The path of the image.
        image_data (bytes): The binary data of the image.
    """
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    depth = Column(Integer, unique=True, index=True)
    path = Column(String, index=True)
    image_data = Column(LargeBinary)  # Storing image data as binary

Base.metadata.create_all(bind=engine)