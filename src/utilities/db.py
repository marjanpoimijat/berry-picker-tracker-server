from dotenv import load_dotenv
from get_docker_secret import get_docker_secret
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

docker_db_url = os.getenv("DATABASE_URL")
if docker_db_url is None:
    docker_db_url = os.environ.get("DATABASE_URI")
env_db_name = os.environ.get("DATABASE_NAME")
env_db_user = os.environ.get("DATABASE_USER")
env_db_pass = os.environ.get("DATABASE_PASS")
env_db_host = os.environ.get("DATABASE_HOST")
env_db_port = os.environ.get("DATABASE_PORT")

engine = create_engine(docker_db_url)

# Create database session (given arguments for configurating session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# New base class that all database relational objects inherit
Base = declarative_base()

# Create database tables based on models.py file
Base.metadata.create_all(bind=engine)
