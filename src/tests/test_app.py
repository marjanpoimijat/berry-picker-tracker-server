"""App tests"""
import os
import re
import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utilities.db import Base
from main import app, get_db


TEST_DATABASE_URI = os.getenv("TEST_DATABASE_URI")

engine = create_engine(TEST_DATABASE_URI)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Test database configuration"""
    try:
        Base.metadata.create_all(bind=engine)
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_connecting_non_existing_url():
    """Routing fails with wrong url"""
    res = client.get("/wrong_url")
    assert res.status_code == 404


def test_connection_works():
    """Routing works with correct url"""
    res = client.get("/")
    assert res.status_code == 200


def test_create_and_get_users_with_generated_id():
    """User creation without given id works correctly"""
    res1 = client.post("/new-user", json={})
    res2 = client.post("/new-user", json={})

    assert res1.status_code == 200
    assert res2.status_code == 200

    res1_id = res1.json()["id"]
    res2_id = res2.json()["id"]

    res1 = client.get("/get-user", headers={"user-id": res1_id})
    res2 = client.get("/get-user", headers={"user-id": res2_id})

    assert res1.status_code == 200
    assert res2.status_code == 200

    assert res1.json()[0]["id"] == res1_id
    assert res2.json()[0]["id"] == res2_id


def test_create_and_get_users_with_given_id():
    """User creation with given id works correctly"""
    res1_post = client.post("/new-user", json={"id": "a1b2c3d4e5f6"})
    res2_post = client.post("/new-user", json={"id": "6f5e4d3c2b1a"})

    assert res1_post.status_code == 200
    assert res2_post.status_code == 200

    res1_post_id = res1_post.json()["id"]
    res2_post_id = res2_post.json()["id"]

    res1_get = client.get("/get-user", headers={"user-id": res1_post_id})
    res2_get = client.get("/get-user", headers={"user-id": res2_post_id})

    assert res1_get.status_code == 200
    assert res2_get.status_code == 200

    assert res1_get.json()[0]["id"] == res1_post_id
    assert res2_get.json()[0]["id"] == res2_post_id


def test_create_route_for_user_with_generated_id_and_get_user():
    """User route creation without given id works correctly"""
    res_post = client.post("/start-route", json={"user_id": "a1b2c3d4e5f6"})

    assert res_post.status_code == 200

    route_id = res_post.json()["id"]
    res_get = client.get("/get-route", headers={"route-id": route_id})

    assert res_get.status_code == 200
    assert res_get.json()[0]["id"] == route_id


def test_create_route_for_user_with_given_id_and_get_route():
    """User route creation with given id works correctly"""
    res_post = client.post(
        "/start-route",
        json={
            "user_id": "a1b2c3d4e5f6",
            "id": "r1r2r3r4r5r6",
        },
    )

    assert res_post.status_code == 200

    route_id = res_post.json()["id"]
    res_get = client.get("/get-route", headers={"route-id": route_id})

    assert res_get.status_code == 200
    assert res_get.json()[0]["id"] == route_id


def test_create_user_and_route_with_generated_id_and_id_is_in_nanoid_form():
    """User and user route creation with given nanoid works correctly"""
    res_user = client.post("/new-user", json={})

    assert res_user.status_code == 200

    user_id = res_user.json()["id"]

    res_route = client.post("/start-route", json={"user_id": user_id})

    assert res_route.status_code == 200

    route_id = res_route.json()["id"]

    pattern = re.compile(r"^[A-Za-z0-9']{12}$")

    user_id_matches = bool(pattern.match(user_id))
    route_id_matches = bool(pattern.match(route_id))

    assert user_id_matches
    assert route_id_matches


def test_create_route_with_non_existent_user():
    """Route creation fails with non-existent user"""
    res_post = client.post("/start-route", json={"user_id": "safsafas"})

    assert res_post.status_code == 404


def test_get_users_routes():
    """User route fetching works correctly"""
    res_get = client.get("/get-user-routes", headers={"user-id": "a1b2c3d4e5f6"})

    assert res_get.status_code == 200
    assert len(res_get.json()) == 2


def test_deactivate_route():
    """Route deactivation works correctly"""
    res_patch = client.patch(
        "/deactivate-route",
        headers={"route-id": "r1r2r3r4r5r6"},
    )

    assert res_patch.status_code == 200

    route_id = res_patch.json()["id"]

    res_get = client.get("/get-route", headers={"route-id": route_id})

    assert res_get.status_code == 200
    assert res_get.json()[0]["active"] is False


def test_create_waypoints_to_route_and_get_routes_waypoints():
    """Waypoint creation works correctly"""
    res_post_route = client.post(
        "/start-route",
        json={
            "user_id": "a1b2c3d4e5f6",
            "id": "6r5r4r3r2r1r",
        },
    )

    assert res_post_route.status_code == 200

    route_id = res_post_route.json()["id"]

    res_post_coord = client.post(
        "/create-waypoint",
        json=[
            {
                "route_id": route_id,
                "latitude": "1.0",
                "longitude": "1.0",
                "mnc": 200,
                "connection": "1g",
            }
        ],
    )

    assert res_post_coord.status_code == 200
    assert res_post_coord.json()[0]["latitude"] == "1.0"
    assert res_post_coord.json()[0]["longitude"] == "1.0"
    assert res_post_coord.json()[0]["connection"] == "1g"

    time.sleep(1)

    res_post_coord = client.post(
        "/create-waypoint",
        json=[
            {
                "route_id": route_id,
                "latitude": "1.1",
                "longitude": "1.1",
                "mnc": 200,
                "connection": "2g",
            }
        ],
    )
    assert res_post_coord.status_code == 200
    assert res_post_coord.json()[0]["latitude"] == "1.1"
    assert res_post_coord.json()[0]["longitude"] == "1.1"
    assert res_post_coord.json()[0]["connection"] == "2g"

    time.sleep(1)

    res_post_coord = client.post(
        "/create-waypoint",
        json=[
            {
                "route_id": route_id,
                "latitude": "1.2",
                "longitude": "1.2",
                "mnc": 200,
                "connection": "3g",
            }
        ],
    )
    assert res_post_coord.status_code == 200
    assert res_post_coord.json()[0]["latitude"] == "1.2"
    assert res_post_coord.json()[0]["longitude"] == "1.2"
    assert res_post_coord.json()[0]["connection"] == "3g"

    time.sleep(1)

    res_post_coord = client.post(
        "/create-waypoint",
        json=[
            {
                "route_id": route_id,
                "latitude": "1.3",
                "longitude": "1.3",
                "mnc": 200,
                "connection": "4g",
            }
        ],
    )

    assert res_post_coord.status_code == 200
    assert res_post_coord.json()[0]["latitude"] == "1.3"
    assert res_post_coord.json()[0]["longitude"] == "1.3"
    assert res_post_coord.json()[0]["connection"] == "4g"

    res_get_route_waypoints = client.get(
        "/get-route-waypoints", headers={"route-id": route_id}
    )

    assert res_get_route_waypoints.status_code == 200
    assert len(res_get_route_waypoints.json()) == 4


def test_get_routes_first_and_latest_waypoint():
    """Get routes first and newest waypoints"""
    route_id = "6r5r4r3r2r1r"
    res_get_route_waypoints = client.get(
        "/get-route-waypoints", headers={"route-id": route_id}
    )

    assert res_get_route_waypoints.status_code == 200

    waypoints = res_get_route_waypoints.json()

    assert (
        waypoints[0]["ts"]
        < waypoints[1]["ts"]
        < waypoints[2]["ts"]
        < waypoints[3]["ts"]
    )


def test_waypoint_timestamp_can_be_given():
    """Waypoint timestamp fetching works correctly"""
    route_id = "6r5r4r3r2r1r"
    timestamp = "2077-10-23T09:47:00"

    res_post_waypoint = client.post(
        "/create-waypoint",
        json=[
            {
                "route_id": route_id,
                "latitude": "1.4",
                "longitude": "1.4",
                "mnc": 200,
                "ts": timestamp,
                "connection": "5g",
            }
        ],
    )

    assert res_post_waypoint.status_code == 200

    res_get_route_waypoints = client.get(
        "/get-route-waypoints", headers={"route-id": route_id}
    )

    assert len(res_get_route_waypoints.json()) == 5
    assert res_get_route_waypoints.json()[4]["ts"] == timestamp


def test_different_connection_types_are_in_database_entries():
    """Network connection types are stored correctly"""
    route_id = "6r5r4r3r2r1r"

    res_get_route_waypoints = client.get(
        "/get-route-waypoints", headers={"route-id": route_id}
    )

    assert res_get_route_waypoints.status_code == 200

    coordinates = res_get_route_waypoints.json()

    assert coordinates[0]["connection"] == "1g"
    assert coordinates[1]["connection"] == "2g"
    assert coordinates[2]["connection"] == "3g"
    assert coordinates[3]["connection"] == "4g"
    assert coordinates[4]["connection"] == "5g"


def test_null_connection_can_be_given():
    """Network connection type null is stored correctly in the database"""
    route_id = "6r5r4r3r2r1r"
    timestamp = "2777-10-23T09:47:00"

    res_post_waypoint = client.post(
        "/create-waypoint",
        json=[
            {
                "route_id": route_id,
                "latitude": "1.5",
                "longitude": "1.5",
                "mnc": 200,
                "ts": timestamp,
                "connection": None,
            }
        ],
    )

    assert res_post_waypoint.status_code == 200

    res_get_route_waypoints = client.get(
        "/get-route-waypoints", headers={"route-id": route_id}
    )

    assert res_get_route_waypoints.status_code == 200
    assert res_get_route_waypoints.json()[5]["connection"] is None


def test_null_mnc_can_be_given():
    """The mobile network code is fetchable from database"""
    route_id = "6r5r4r3r2r1r"
    timestamp = "2888-10-23T09:47:00"

    res_post_waypoint = client.post(
        "/create-waypoint",
        json=[
            {
                "route_id": route_id,
                "latitude": "1.6",
                "longitude": "1.6",
                "mnc": None,
                "ts": timestamp,
                "connection": "5g",
            }
        ],
    )

    assert res_post_waypoint.status_code == 200

    res_get_route_waypoints = client.get(
        "/get-route-waypoints", headers={"route-id": route_id}
    )

    assert res_get_route_waypoints.status_code == 200
    assert res_get_route_waypoints.json()[6]["mnc"] is None


def test_no_connection_waypoint_can_be_given():
    """Waypoint created while without network connection gets stored correctly"""
    route_id = "6r5r4r3r2r1r"
    timestamp = "3077-10-23T09:47:00"

    res_post_waypoint = client.post(
        "/create-waypoint",
        json=[
            {
                "route_id": route_id,
                "latitude": "1.7",
                "longitude": "1.7",
                "mnc": None,
                "ts": timestamp,
                "connection": None,
            }
        ],
    )

    assert res_post_waypoint.status_code == 200

    res_get_route_waypoints = client.get(
        "/get-route-waypoints", headers={"route-id": route_id}
    )

    assert res_get_route_waypoints.status_code == 200
    assert res_get_route_waypoints.json()[7]["mnc"] is None
    assert res_get_route_waypoints.json()[7]["connection"] is None


def test_get_users_latest_routes_waypoints():
    """Waypoints from the user's latest route are fetchable"""
    user_id = "a1b2c3d4e5f6"

    res_waypoints = client.get("/get-users-latest-route/", headers={"user-id": user_id})

    assert res_waypoints.status_code == 200

    is_active = res_waypoints.json()[1]
    waypoints = res_waypoints.json()[2]

    assert len(waypoints) == 8
    assert is_active is True

    assert waypoints[0]["latitude"] == "1.0"
    assert waypoints[0]["longitude"] == "1.0"

    assert waypoints[len(waypoints) - 1]["latitude"] == "1.7"
    assert waypoints[len(waypoints) - 1]["longitude"] == "1.7"


def test_delete_route():
    "Route deletion works correctly"
    route_id = "6r5r4r3r2r1r"
    res_get_route = client.get("/get-route", headers={"route-id": route_id})

    assert res_get_route.status_code == 200
    assert len(res_get_route.json()) == 1

    res_delete_route = client.delete("/delete-route", headers={"route-id": route_id})

    assert res_delete_route.status_code == 200
    assert res_delete_route.json() == 1

    res_get_route = client.get("/get-route", headers={"route-id": route_id})

    assert res_get_route.status_code == 200
    assert len(res_get_route.json()) == 0


def test_no_latest_route_found_on_non_existent_user():
    """Non-existent user has no routes"""
    res_waypoints = client.get(
        "/get-users-latest-route", headers={"user-id": "111111111111"}
    )

    custom_error_message = res_waypoints.json()["detail"]

    assert res_waypoints.status_code == 404
    assert custom_error_message == "User or no routes found"


def test_no_latest_route_found_on_user_with_no_routes():
    """No routes are returned if user has no routes in database"""
    user_id = "a1a1a1a1a1a1"
    res_new_user = client.post("/new-user", json={"id": user_id})

    assert res_new_user.status_code == 200
    assert res_new_user.json()["id"] == user_id

    res_waypoints = client.get("/get-users-latest-route/", headers={"user-id": user_id})

    custom_error_message = res_waypoints.json()["detail"]

    assert res_waypoints.status_code == 404
    assert custom_error_message == "User or no routes found"


def test_delete_user():
    """User deletion works"""
    user_id = "a1b2c3d4e5f6"
    res_get_user = client.get("/get-user", headers={"user-id": user_id})

    assert res_get_user.status_code == 200
    assert len(res_get_user.json()) == 1

    res_get_routes = client.get("/get-user-routes", headers={"user-id": user_id})

    assert res_get_routes.status_code == 200
    assert len(res_get_routes.json()) == 2

    res_delete_user = client.delete("/delete-user", headers={"user-id": user_id})

    assert res_delete_user.status_code == 200
    assert res_delete_user.json() == 1

    res_get_user = client.get("/get-user", headers={"user-id": user_id})

    assert res_get_user.status_code == 200
    assert len(res_get_user.json()) == 0

    res_get_routes = client.get("/get-user-routes", headers={"user-id": user_id})

    assert res_get_routes.status_code == 200
    assert len(res_get_routes.json()) == 0


Base.metadata.drop_all(engine)
