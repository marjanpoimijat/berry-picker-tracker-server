"""Module for defining database objects"""
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import relationship


from .db import Base


class User(Base):
    """Database user object"""

    __tablename__ = "users"

    id = Column(String, primary_key=True, unique=True, nullable=False)

    routes = relationship(
        "Route", back_populates="user", cascade="all, delete", passive_deletes=True
    )


class Route(Base):
    """Database route object"""

    __tablename__ = "routes"

    id = Column(String, primary_key=True, unique=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    active = Column(Boolean)

    user = relationship("User", back_populates="routes")
    waypoints = relationship(
        "Waypoint",
        back_populates="route",
        cascade="all, delete",
        passive_deletes=True,
    )


class Waypoint(Base):
    """Database waypoint object"""

    def __str__(self):
        return f"""
            Waypoint(
                route_id={self.route_id},
                latitude={self.latitude},
                longitude={self.longitude},
                mnc={self.mnc},
                ts={self.ts},
                connection={self.connection}
            )
        """

    __tablename__ = "waypoints"

    route_id = Column(
        String, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False
    )
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    mnc = Column(Integer, nullable=True)
    ts = Column(DateTime)
    connection = Column(String, nullable=True)

    __table_args__ = (PrimaryKeyConstraint(route_id, ts), {})

    route = relationship("Route", back_populates="waypoints")
