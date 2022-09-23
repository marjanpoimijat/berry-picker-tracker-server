from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base

# Database objects defined


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column("password", String, nullable=False)

    coordinates = relationship("Coordinate", back_populates="user")


class Coordinate(Base):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    ts = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="coordinates")
