from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import relationship


from .db import Base

# Database objects defined


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, unique=True, nullable=False)

    routes = relationship(
        "Route", back_populates="user", cascade="all, delete", passive_deletes=True
    )


class Route(Base):
    __tablename__ = "routes"

    id = Column(String, primary_key=True, unique=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    active = Column(Boolean)

    user = relationship("User", back_populates="routes")
    waypoints = relationship(
        "Waypoint",
        back_populates="route",
        cascade="all, delete",
        passive_deletes=True,
    )


class Waypoint(Base):
    __tablename__ = "waypoints"

    route_id = Column(
        String, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False
    )
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    mnc = Column(Integer)
    ts = Column(DateTime)

    __table_args__ = (PrimaryKeyConstraint(route_id, ts), {})

    route = relationship("Route", back_populates="waypoints")
