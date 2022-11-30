from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from nanoid import generate


# This file is basically just for data validation


def get_nanoid():
    """Generate nanoid as a string"""
    return str(
        generate("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 12)
    )


def get_timestamp():
    """Generate timestamp"""
    return datetime.now()


class WaypointBase(BaseModel):
    """Common attributes for Waypoint objects"""

    route_id: str
    latitude: float
    longitude: float
    mnc: int = Field(None, description="No MNC code")
    ts: datetime = Field(default_factory=get_timestamp)
    connection: Optional[str] = Field(None, description="No connection")


class WaypointCreate(WaypointBase):
    # Creating waypoints does not need additional data
    pass


class Waypoint(WaypointBase):
    """Attributes (addition to WaypointteBase) that are seen when reading data"""

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RouteBase(BaseModel):
    """Common attributes for Route objects"""

    id: str = Field(default_factory=get_nanoid)
    user_id: str
    active: bool = True


class RouteCreate(RouteBase):
    # Creating routes does not need additional data
    pass


class Route(RouteBase):
    """Attributes (Addition to RouteBase) that are seen when reading data"""

    waypoints: List[Waypoint] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserBase(BaseModel):
    """Common attributes for User objects"""

    id: str = Field(default_factory=get_nanoid)


class UserCreate(UserBase):
    # Creating user does not need additional data
    pass


class User(UserBase):
    """Attributes (addition to UserBase and UserCreate) that are seen when reading data"""

    routes: List[Route] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
