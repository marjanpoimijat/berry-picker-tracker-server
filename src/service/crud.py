from sqlalchemy.orm import Session

import utilities.models as models
import utilities.schemas as schemas

# All CRUD methods take current database session as an argument
# and additional parameters (path parameters etc.). crud.py as a service layer. Main.py methods always
# call crud.py operations


def get_users(db: Session):
    """Get all users"""
    return db.query(models.User).all()


def get_user(db: Session, user_id: int):
    """Get user by user_id (given as a path parameter)"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    """Adds user to DB, takes json body as a parameter and compares (and validates) it according to schemas.py file's models"""
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_coordinates(db: Session):
    """Get all coordinates"""
    return db.query(models.Coordinate).all()


def create_coordinate(db: Session, coordinate: schemas.CoordinateCreate, user_id: int):
    """Adds coordinate to DB and relates it to some user. takes json body as a parameter and compares (and validates) it according to schemas.py file's models"""
    db_coordinate = models.Coordinate(**coordinate.dict(), user_id=user_id)

    db.add(db_coordinate)
    db.commit()
    db.refresh(db_coordinate)

    return db_coordinate


def get_user_coordinates(db: Session, user_id: int):
    """Get user's coordinates using user_id"""
    return db.query(models.Coordinate).filter(models.Coordinate.id == user_id).all()
