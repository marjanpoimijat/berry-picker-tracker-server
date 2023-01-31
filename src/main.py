import requests
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Response, HTTPException, Depends, Header
from fastapi.responses import RedirectResponse
from typing import List
from sqlalchemy.orm import Session

from service import crud
from utilities import schemas
from utilities.db import SessionLocal
from utilities.db import Base, engine

load_dotenv()
API_KEY = os.environ.get("NLS_API_KEY")
LEGEND_URI = os.environ.get("LEGEND_URI")
REV_NUMBER = os.environ.get("CODE_REVISION", "unknown")
SERVER_ENV = os.environ.get("SERVER_ENVIRONMENT", "development")
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


@app.get("/server-version")
def get_rev_number():
    """Display the revision id and build date etc"""
    is_dev = SERVER_ENV == "development"
    details = (
        "Local development"
        if is_dev
        else f"Code revision: {REV_NUMBER}\nRunning in {SERVER_ENV}"
    )
    return f"Berry Picker Tracker Server\n{details}"


@app.get("/osmapi/{z}/{y}/{x}")
def get_nls_tile(z, y, x):
    url = "http://a.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png".format(
        z=z, y=y, x=x
    )
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return Response(
            content=response.content, media_type="image/png", status_code=200
        )
    raise HTTPException(status_code=404, detail="Image not found.")


@app.get("/nlsapi/{z}/{y}/{x}")
def get_nls_tile(z, y, x):
    url = "https://avoin-karttakuva.maanmittauslaitos.fi/avoin/wmts/1.0.0/maastokartta/default/WGS84_Pseudo-Mercator/{z}/{y}/{x}.png".format(
        z=z, y=y, x=x
    )
    response = requests.get(url, auth=(API_KEY, ""), stream=True)
    if response.status_code == 200:
        return Response(
            content=response.content, media_type="image/png", status_code=200
        )
    raise HTTPException(status_code=404, detail="Image not found.")


@app.post("/new-user/")
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create new user session"""
    return crud.create_user(user, db)


@app.post("/start-route/")
def create_new_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    """Create a new route for the user given in route object"""
    db_route = crud.create_new_route(route, db)

    if db_route is False:
        raise HTTPException(
            status_code=404, detail="User not found, can't start a route"
        )

    return db_route


@app.post("/create-waypoint/")
def create_new_waypoint(
    waypoints: List[schemas.WaypointCreate], db: Session = Depends(get_db)
):
    """Create a new waypoint for the route (route_id given in Waypoint object)"""
    return crud.create_new_waypoint(waypoints, db)


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
    """Get user's route by user_id, provides user_id via custom header"""
    return crud.get_users_routes(user_id, db)


@app.get("/get-users-latest-route/")
def get_user_latest_route(user_id: str = Header(), db: Session = Depends(get_db)):
    """Get user's latest route, regardless of it being active or not"""
    waypoints = crud.get_users_latest_route(user_id, db)

    if waypoints is False:
        raise HTTPException(status_code=404, detail="User or no routes found")

    return crud.get_users_latest_route(user_id, db)


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


@app.get("/get-legend/")
def get_legend():
    print(LEGEND_URI)
    return RedirectResponse(LEGEND_URI)
