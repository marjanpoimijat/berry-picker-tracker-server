from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from service import crud
from utilities import schemas
from utilities.db import SessionLocal
from utilities.db import Base, engine

"""Create tables and get db session"""

app = FastAPI()


def get_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""Root's warmest welcome"""


@app.get("/")
def redirect_root():
    return "G'day"


"""Create user and compare sent body to schema's model"""


@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


"""Get user by user_id and specify response as a User object"""


@app.get("/get_user/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)


"""Get all users"""


@app.get("/get_users/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


"""Post coordinates and compare sent body to schema's model, user_id given as a path parameter"""


@app.post("/coordinates/{user_id}")
def create_coordinate(
    user_id: int, coordinate: schemas.CoordinateCreate, db: Session = Depends(get_db)
):
    return crud.create_coordinate(db=db, coordinate=coordinate, user_id=user_id)


"""Get all coordinates"""


@app.get("/get_coordinates/", response_model=List[schemas.Coordinate])
def get_coordinates(db: Session = Depends(get_db)):
    return crud.get_coordinates(db=db)


"""Get user's coordinates by given user_id"""


@app.get("/get_coordinates/{user_id}", response_model=List[schemas.Coordinate])
def get_user_coordinates(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_coordinates(db=db, user_id=user_id)
