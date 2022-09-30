from datetime import datetime
from typing import List, Union
from pydantic import BaseModel, Field
from uuid import uuid4


# This file is basically just for data validation


def get_uuid():
    """Generate uuid4 as a string"""
    return str(uuid4())


class CoordinateBase(BaseModel):
    """Common attributes for Coordinate objects"""

    route_id: str
    latitude: float
    longitude: float
    mnc: int


class CoordinateCreate(CoordinateBase):
    # Creating coordinates does not need additional data
    pass


class Coordinate(CoordinateBase):
    """Attributes (addition to CoordinateBase) that are seen when reading data"""

    id: int
    ts: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RouteBase(BaseModel):
    """Common attributes for Route objects"""

    id: str = Field(default_factory=get_uuid)
    user_id: str
    active: bool = True


class RouteCreate(RouteBase):
    # Creating routes does not need additional data
    pass


class Route(RouteBase):
    """Attributes (Addition to RouteBase) that are seen when reading data"""

    coordinates: List[Coordinate] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserBase(BaseModel):
    """Common attributes for User objects"""

    id: str = Field(default_factory=get_uuid)


class UserCreate(UserBase):
    # Creating user does not need additional data
    pass


class User(UserBase):
    """Attributes (addition to UserBase and UserCreate) that are seen when reading data"""

    routes: List[Route] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
