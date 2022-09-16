import os

from dotenv import load_dotenv
from fastapi import FastAPI
from service.service import Service
from pydantic import BaseModel


load_dotenv()
database_uri = os.environ.get("DATABASE_URI")

app = FastAPI()
service = Service(database_uri)

class Coordinates(BaseModel):
    """Pydantic data validation, coordinate data should be given in this form"""
    latitude: float
    longitude: float

class User(BaseModel):
    """Pydantic data validation, user data should be given in this form"""
    username: str
    passwd: str


@app.get("/")
def get_root():
    """Root's warmest greetings"""
    return {"Hello": "World"}

@app.get("/all")
def get_all():
    """Get all coordinate database entries"""
    return service.get_all_coordinate_entries()

@app.get("/getcoordinates/{user_id}")
def get_users_coordinates(user_id: int):
    """Get users coordinates with given user_id"""
    return service.get_users_coordinates(user_id)
     
@app.post("/postcoordinates/{user_id}")
def create_coordinate(coordinates: Coordinates, user_id: int):
    """Create new coordinates entry with given user_id"""
    return service.create_coordinates(user_id, coordinates.latitude, coordinates.longitude)

@app.post("/createuser/")
def create_user(user: User):
    """"Create new user"""
    return service.create_user(user.username, user.passwd)
    