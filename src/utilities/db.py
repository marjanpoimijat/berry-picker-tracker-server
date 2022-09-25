from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URI = os.environ.get("DATABASE_URI")

# Create database engine according to the database uri
engine = create_engine(DATABASE_URI)

# Create database session (given arguments for configurating session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# New base class that all database relational objects inherit
Base = declarative_base()

# Create database tables based on models.py file
Base.metadata.create_all(bind=engine)
