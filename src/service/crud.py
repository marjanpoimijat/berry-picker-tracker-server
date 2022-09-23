from sqlalchemy.orm import Session

import utilities.models as models
import utilities.schemas as schemas

# All CRUD methods take current database session as an argument
# and additional parameters (path parameters etc.). crud.py as a service layer. Main.py methods always
# call crud.py operations"""

"""Get all users"""


def get_users(db: Session):
    return db.query(models.User).all()


"""Get user by user_id (given as a path parameter)"""


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


"""Adds user to DB, takes json body as a parameter and compares (and validates) it according to schemas.py file's models"""


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


"""Get all coordinates"""


def get_coordinates(db: Session):
    return db.query(models.Coordinate).all()


"""Adds coordinate to DB and relates it to some user. takes json body as a parameter and compares (and validates) it according to schemas.py file's models"""


def create_coordinate(db: Session, coordinate: schemas.CoordinateCreate, user_id: int):
    db_coordinate = models.Coordinate(**coordinate.dict(), user_id=user_id)

    db.add(db_coordinate)
    db.commit()
    db.refresh(db_coordinate)

    return db_coordinate


"""Get user's coordinates using user_id"""


def get_user_coordinates(db: Session, user_id: int):
    return db.query(models.Coordinate).filter(models.Coordinate.id == user_id).all()
