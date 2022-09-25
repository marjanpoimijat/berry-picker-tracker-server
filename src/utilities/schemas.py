from datetime import datetime
from typing import List
from pydantic import BaseModel

# This file is basically just for data validation


class CoordinateBase(BaseModel):
    """Common attributes for Coordinate objects"""

    latitude: float
    longitude: float


class CoordinateCreate(CoordinateBase):
    # Creating coordinates does not need additional data
    pass


class Coordinate(CoordinateBase):
    """Attributes (addition to CoordinateBase) that are seen when reading data"""

    id: int
    user_id: int
    ts: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserBase(BaseModel):
    """Common attributes for User objects"""

    username: str


class UserCreate(UserBase):
    """Attributes that are needed for creating but not for reading data"""

    password: str


class User(UserBase):
    """Attributes (addition to UserBase and UserCreate) that are seen when reading data"""

    id: int
    coordinates: List[Coordinate] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
