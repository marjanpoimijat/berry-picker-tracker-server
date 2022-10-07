from dotenv import load_dotenv
from get_docker_secret import get_docker_secret
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

docker_db_passwd = get_docker_secret("db-passwd")
env_db_uri = os.environ.get("DATABASE_URI")

engine = create_engine(
    env_db_uri
    if docker_db_passwd is None
    else f"postgresql://postgres:{docker_db_passwd}@database/bpt"
)

# Create database session (given arguments for configurating session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# New base class that all database relational objects inherit
Base = declarative_base()

# Create database tables based on models.py file
Base.metadata.create_all(bind=engine)
