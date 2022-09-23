from datetime import datetime
from typing import List
from pydantic import BaseModel

# This file is basically just for data validation

"""Common attributes for Coordinate objects"""


class CoordinateBase(BaseModel):
    latitude: float
    longitude: float


"""Creating coordinates does not need additional data"""


class CoordinateCreate(CoordinateBase):
    pass


"""Attributes (addition to CoordinateBase) that are seen when reading data"""


class Coordinate(CoordinateBase):
    id: int
    user_id: int
    ts: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


"""Common attributes for User objects"""


class UserBase(BaseModel):
    username: str


"""Attributes that are needed for creating but not for reading data"""


class UserCreate(UserBase):
    password: str


"""Attributes (addition to UserBase and UserCreate) that are seen when reading data"""


class User(UserBase):
    id: int
    coordinates: List[Coordinate] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
