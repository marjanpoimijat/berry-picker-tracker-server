from typing import List

from fastapi import FastAPI, Depends, Query, Header
from sqlalchemy.orm import Session

from service import crud
from utilities import schemas
from utilities.db import SessionLocal
from utilities.db import Base, engine


app = FastAPI()


def get_db():
    """Create tables (if does not exist) and get db session"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def redirect_root():
    """Root's warmest welcome"""
    return "G'day"


@app.post("/new-user/")
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create new user session"""
    return crud.create_user(user, db)


@app.post("/start-route/")
def create_new_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    """Create a new route for the user given in route object"""
    return crud.create_new_route(route, db)


# Have to think about some system to post waypoints if many waypoints posted at the same time (like after being offline for a while)
@app.post("/create-waypoint/")
def create_new_waypoint(
    coordinates: List[schemas.CoordinateCreate], db: Session = Depends(get_db)
):
    """Create a new waypoint for the route (route_id given in coordinate object)"""
    return crud.create_new_waypoint(coordinates, db)


@app.get("/get-user/")
def get_user(user_id: str = Header(), db: Session = Depends(get_db)):
    """Get user by user_id, provides user_id via custom header"""
    return crud.get_user_by_id(user_id, db)


@app.get("/get-route/")
def get_route(route_id: str = Header(), db: Session = Depends(get_db)):
    """Get user by route_id, provides route_id via custom header"""
    return crud.get_route_by_id(route_id, db)


@app.get("/get-user-routes/")
def get_users_route(user_id: str = Header(), db: Session = Depends(get_db)):
    """Get users route by user_id, provides user_id via custom header"""
    return crud.get_users_routes(user_id, db)


@app.get("/get-route-waypoints/")
def get_routes_waypoints(route_id: str = Header(), db: Session = Depends(get_db)):
    """Get routes waypoints by route_id, provides route_id via custom header"""
    return crud.get_routes_waypoints(route_id, db)


@app.patch("/deactivate-route/")
def deactivate_route(route_id: str = Header(), db: Session = Depends(get_db)):
    """Deactivate route (change 'active' column -> false), provides route_id via custom header"""
    return crud.deactivate_route(route_id, db)


@app.delete("/delete-user/")
def delete_user(user_id: str = Header(), db: Session = Depends(get_db)):
    """Delete user by id, provides user_id via custom header"""
    return crud.delete_user(user_id, db)


@app.delete("/delete-route/")
def delete_route(route_id: str = Header(), db: Session = Depends(get_db)):
    """Delete route by id, provides route_id via header"""
    return crud.delete_route(route_id, db)
