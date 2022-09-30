from sqlalchemy.orm import Session

import utilities.models as models
import utilities.schemas as schemas

# All CRUD methods take current database session as an argument
# and additional parameters (path parameters etc.). crud.py as a service layer. Main.py methods always
# calls crud.py operations


def create_user(user: schemas.UserCreate, db: Session):
    """Adds user to DB, takes json body as a parameter and compares (and validates) it according to schemas.py"""
    db_user = models.User(**user.dict())

    _create(db_user, db)

    return db_user


def create_new_route(route: schemas.RouteCreate, db: Session):
    """Add users new route to DB, takes json body as a parameter and compares (and validates) it according to schemas.py"""
    db_route = models.Route(**route.dict())

    _create(db_route, db)

    return db_route


def create_new_waypoint(coordinate: schemas.CoordinateCreate, db: Session):
    """Add routes new waypoint to DB, takes json body as a parameter and compares (and validates) it according to schemas.py"""
    db_waypoint = models.Coordinate(**coordinate.dict())

    _create(db_waypoint, db)

    return db_waypoint


def get_user_by_id(user_id: str, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).all()


def get_route_by_id(route_id: str, db: Session):
    return db.query(models.Route).filter(models.Route.id == route_id).all()


def get_users_routes(user_id: str, db: Session):
    """Get users routes"""
    return db.query(models.Route).filter(models.Route.user_id == user_id).all()


def get_routes_waypoints(route_id: str, db: Session):
    """Get routes waypoints"""
    return (
        db.query(models.Coordinate).filter(models.Coordinate.route_id == route_id).all()
    )


def deactivate_route(route_id: str, db: Session):
    """Changes routes 'active' column to false"""
    try:
        to_update = get_route_by_id(route_id, db)[0]
        to_update.active = False

        db.commit()
        db.refresh(to_update)

        return to_update
    except Exception as e:
        return e


def delete_user(user_id: str, db: Session):
    """Delete user"""
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()


def delete_route(route_id: str, db: Session):
    """Delete route"""
    db.query(models.Route).filter(models.Route.id == route_id).delete()
    db.commit()


def _create(db_object, db: Session):
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
