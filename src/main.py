"""Routing module"""
import os
from typing import List
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Response, HTTPException, Depends, Header
from fastapi.responses import RedirectResponse
from mangum import Mangum
from sqlalchemy.orm import Session

from service import crud
from utilities import schemas
from utilities.db import SessionLocal
from utilities.db import Base, engine

load_dotenv()
API_KEY = os.environ.get("NLS_API_KEY")
if API_KEY is None:
    API_KEY = os.getenv("NLS_API_KEY")
LEGEND_URI = os.environ.get("LEGEND_URI")
app = FastAPI()

# For AWS Lambda
handler = Mangum(app)


def get_db():
    """Create tables (if does not exist) and get db session"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_nls_map(maptype: str, z, y, x):
    """Fetches specified maptiles via the NLS API"""

    url = f"https://avoin-karttakuva.maanmittauslaitos.fi/avoin/wmts/1.0.0/{maptype}/default/WGS84_Pseudo-Mercator/{z}/{y}/{x}.png"
    response = requests.get(url, auth=(API_KEY, ""), stream=True)
    if response.status_code == 200:
        return Response(
            content=response.content, media_type="image/png", status_code=200
        )
    raise HTTPException(status_code=404, detail="Image not found.")


@app.get("/")
def redirect_root():
    """Root's warmest welcome"""
    return "terve"


@app.get("/status")
def get_status():
    """Display the status of the server"""
    return {"subject": "staging status", "status": "OK", "color": "green"}


# for testing purposes only
@app.get("/osmapi/{z}/{y}/{x}")
def get_osm_tile(z, y, x):
    """Fetches specified OpenStreet Map tile"""
    print("osmapi handler called")
    url = f"http://a.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png"
    print("url: ", url)
    response = requests.get(url, stream=True)
    print("response: ", response)
    if response.status_code == 200:
        return Response(
            content=response.content, media_type="image/png", status_code=200
        )
    raise HTTPException(status_code=404, detail="Image not found.")


@app.get("/nlstopographic/{z}/{y}/{x}")
def get_nlsortographic_tile(z, y, x):
    """Get topographic map tile from NLS"""
    response = get_nls_map("maastokartta", z, y, x)
    return response


@app.get("/nlsplain/{z}/{y}/{x}")
def get_nlsplain_tile(z, y, x):
    """Get plain map tile from NLS"""
    response = get_nls_map("selkokartta", z, y, x)
    return response


@app.get("/nlsaerial/{z}/{y}/{x}")
def get_nlsaerial_tile(z, y, x):
    """Get aerial map tile from NLS"""
    response = get_nls_map("ortokuva", z, y, x)
    return response


@app.post("/new-user")
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create new user session"""
    return crud.create_user(user, db)


@app.post("/start-route")
def create_new_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    """Create a new route for the user given in route object"""
    db_route = crud.create_new_route(route, db)

    if db_route is False:
        raise HTTPException(
            status_code=404, detail="User not found, can't start a route"
        )

    return db_route


@app.post("/create-waypoint")
def create_new_waypoint(
    waypoints: List[schemas.WaypointCreate], db: Session = Depends(get_db)
):
    """Create a new waypoint for the route (route_id given in Waypoint object)"""
    return crud.create_new_waypoint(waypoints, db)


@app.get("/get-user")
def get_user(user_id: str = Header(), db: Session = Depends(get_db)):
    """Get user by user_id, provides user_id via custom header"""
    return crud.get_user_by_id(user_id, db)


@app.get("/get-route")
def get_route(route_id: str = Header(), db: Session = Depends(get_db)):
    """Get user by route_id, provides route_id via custom header"""
    return crud.get_route_by_id(route_id, db)


@app.get("/get-user-routes")
def get_users_route(user_id: str = Header(), db: Session = Depends(get_db)):
    """Get user's route by user_id, provides user_id via custom header"""
    return crud.get_users_routes(user_id, db)


@app.get("/get-users-latest-route")
def get_user_latest_route(user_id: str = Header(), db: Session = Depends(get_db)):
    """Get user's latest route, regardless of it being active or not"""
    waypoints = crud.get_users_latest_route(user_id, db)

    if waypoints is False:
        raise HTTPException(status_code=404, detail="User or no routes found")

    return crud.get_users_latest_route(user_id, db)


@app.get("/get-route-waypoints")
def get_routes_waypoints(route_id: str = Header(), db: Session = Depends(get_db)):
    """Get routes waypoints by route_id, provides route_id via custom header"""
    return crud.get_routes_waypoints(route_id, db)


@app.patch("/deactivate-route")
def deactivate_route(route_id: str = Header(), db: Session = Depends(get_db)):
    """Deactivate route (change 'active' column -> false), provides route_id via custom header"""
    return crud.deactivate_route(route_id, db)


@app.delete("/delete-user")
def delete_user(user_id: str = Header(), db: Session = Depends(get_db)):
    """Delete user by id, provides user_id via custom header"""
    return crud.delete_user(user_id, db)


@app.delete("/delete-route")
def delete_route(route_id: str = Header(), db: Session = Depends(get_db)):
    """Delete route by id, provides route_id via header"""
    return crud.delete_route(route_id, db)


@app.get("/get-legend")
def get_legend():
    """Fetches map legend pdf from the NLS website"""
    print(LEGEND_URI)
    return RedirectResponse(LEGEND_URI)
