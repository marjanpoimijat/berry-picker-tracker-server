import json
import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utilities.db import Base
from main import app, get_db

import os
from dotenv import load_dotenv


load_dotenv()

TEST_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")

engine = create_engine(TEST_DATABASE_URI, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        Base.metadata.create_all(bind=engine)
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_connecting_non_existing_url():
    res = client.get("/wrong_url")
    assert res.status_code == 404


def test_connection_works():
    res = client.get("/")
    assert res.status_code == 200


def test_create_and_get_users_with_generated_id():
    res1 = client.post("/new-user/", json={})
    res2 = client.post("/new-user/", json={})

    assert res1.status_code == 200
    assert res2.status_code == 200

    res1_id = res1.json()["id"]
    res2_id = res2.json()["id"]

    res1 = client.get("/get-user/", headers={"user-id": res1_id})
    res2 = client.get("/get-user/", headers={"user-id": res2_id})

    assert res1.status_code == 200
    assert res2.status_code == 200

    assert res1.json()[0]["id"] == res1_id
    assert res2.json()[0]["id"] == res2_id


def test_create_and_get_users_with_given_id():
    res1_post = client.post(
        "/new-user/", json={"id": "12345678-abcd-1234-efgh-123456789000"}
    )
    res2_post = client.post(
        "/new-user/", json={"id": "87654321-dcba-4321-hgfe-000987654321"}
    )

    assert res1_post.status_code == 200
    assert res2_post.status_code == 200

    res1_post_id = res1_post.json()["id"]
    res2_post_id = res2_post.json()["id"]

    res1_get = client.get("/get-user/", headers={"user-id": res1_post_id})
    res2_get = client.get("/get-user/", headers={"user-id": res2_post_id})

    assert res1_get.status_code == 200
    assert res2_get.status_code == 200

    assert res1_get.json()[0]["id"] == res1_post_id
    assert res2_get.json()[0]["id"] == res2_post_id


def test_create_route_for_user_with_generated_id_and_get_user():
    res_post = client.post(
        "/start-route/", json={"user_id": "12345678-abcd-1234-efgh-123456789000"}
    )

    assert res_post.status_code == 200

    route_id = res_post.json()["id"]
    res_get = client.get("/get-route/", headers={"route-id": route_id})

    assert res_get.status_code == 200
    assert res_get.json()[0]["id"] == route_id


def test_create_route_for_user_with_given_id_and_get_route():
    res_post = client.post(
        "/start-route/",
        json={
            "user_id": "12345678-abcd-1234-efgh-123456789000",
            "id": "1111111-abcd-1111-efgh-111111111111",
        },
    )

    assert res_post.status_code == 200

    route_id = res_post.json()["id"]
    res_get = client.get("/get-route/", headers={"route-id": route_id})

    assert res_get.status_code == 200
    assert res_get.json()[0]["id"] == route_id


def test_get_users_routes():
    res_get = client.get(
        "/get-user-routes", headers={"user-id": "12345678-abcd-1234-efgh-123456789000"}
    )

    assert res_get.status_code == 200
    assert len(res_get.json()) == 2


def test_deactivate_route():
    res_patch = client.patch(
        "/deactivate-route/",
        headers={"route-id": "1111111-abcd-1111-efgh-111111111111"},
    )

    assert res_patch.status_code == 200

    route_id = res_patch.json()["id"]

    res_get = client.get("/get-route/", headers={"route-id": route_id})

    assert res_get.status_code == 200
    assert res_get.json()[0]["active"] == False


def test_create_waypoints_to_route_and_get_routes_waypoints():
    res_post_route = client.post(
        "/start-route/",
        json={
            "user_id": "12345678-abcd-1234-efgh-123456789000",
            "id": "22222222-2a2a-2222-2b2b-222222222222",
        },
    )

    assert res_post_route.status_code == 200

    route_id = res_post_route.json()["id"]

    res_post_coord = client.post(
        "/create-waypoint/",
        json=[{"route_id": route_id, "latitude": 1.0, "longitude": 1.0, "mnc": 200}],
    )

    assert res_post_coord.status_code == 200
    assert res_post_coord.json()[0]["latitude"] == 1.0
    assert res_post_coord.json()[0]["longitude"] == 1.0

    time.sleep(1)

    res_post_coord = client.post(
        "/create-waypoint/",
        json=[{"route_id": route_id, "latitude": 1.1, "longitude": 1.1, "mnc": 200}],
    )
    assert res_post_coord.status_code == 200
    assert res_post_coord.json()[0]["latitude"] == 1.1
    assert res_post_coord.json()[0]["longitude"] == 1.1

    time.sleep(1)

    res_post_coord = client.post(
        "/create-waypoint/",
        json=[{"route_id": route_id, "latitude": 1.2, "longitude": 1.2, "mnc": 200}],
    )
    assert res_post_coord.status_code == 200
    assert res_post_coord.json()[0]["latitude"] == 1.2
    assert res_post_coord.json()[0]["longitude"] == 1.2

    time.sleep(1)

    res_post_coord = client.post(
        "/create-waypoint/",
        json=[{"route_id": route_id, "latitude": 1.3, "longitude": 1.3, "mnc": 200}],
    )

    assert res_post_coord.status_code == 200
    assert res_post_coord.json()[0]["latitude"] == 1.3
    assert res_post_coord.json()[0]["longitude"] == 1.3

    res_get_route_waypoints = client.get(
        "/get-route-waypoints/", headers={"route-id": route_id}
    )

    assert len(res_get_route_waypoints.json()) == 4


def test_get_routes_first_and_latest_waypoint():
    route_id = "22222222-2a2a-2222-2b2b-222222222222"
    res_get_route_waypoints = client.get(
        "/get-route-waypoints/", headers={"route-id": route_id}
    )

    assert res_get_route_waypoints.status_code == 200

    coordinates = res_get_route_waypoints.json()

    assert (
        coordinates[0]["ts"]
        < coordinates[1]["ts"]
        < coordinates[2]["ts"]
        < coordinates[3]["ts"]
    )


def test_delete_route():
    route_id = "22222222-2a2a-2222-2b2b-222222222222"
    res_get_route = client.get("/get-route/", headers={"route-id": route_id})

    assert res_get_route.status_code == 200
    assert len(res_get_route.json()) == 1

    res_delete_route = client.delete("/delete-route/", headers={"route-id": route_id})

    assert res_delete_route.status_code == 200

    res_get_route = client.get("/get-route/", headers={"route-id": route_id})

    assert res_get_route.status_code == 200
    assert len(res_get_route.json()) == 0


def test_delete_user():
    user_id = "12345678-abcd-1234-efgh-123456789000"
    res_get_user = client.get("/get-user/", headers={"user-id": user_id})

    assert res_get_user.status_code == 200
    assert len(res_get_user.json()) == 1

    res_delete_user = client.delete("/delete-user/", headers={"user-id": user_id})

    assert res_delete_user.status_code == 200

    res_get_user = client.get("/get-user/", headers={"user-id": user_id})

    assert res_get_user.status_code == 200
    assert len(res_get_user.json()) == 0


def test_remove_db():
    os.remove("test.db")

    assert os.path.exists("test.db") == False
