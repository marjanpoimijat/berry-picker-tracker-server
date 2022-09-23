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


def test_create_and_get_users():
    res1 = client.post(
        "/users/",
        json={"username": "test_user1", "password": "test_password1"},
    )
    res2 = client.post(
        "/users/", json={"username": "test_user2", "password": "test_password2"}
    )

    json_data1 = res1.json()
    json_data2 = res2.json()

    user_id1 = json_data1["id"]
    user_id2 = json_data2["id"]

    assert res1.status_code == 200
    assert json_data1["username"] == "test_user1"

    assert res2.status_code == 200
    assert json_data2["username"] == "test_user2"

    res1 = client.get(f"/get_user/{user_id1}")
    res2 = client.get(f"/get_user/{user_id2}")

    assert res1.status_code == 200
    assert res2.status_code == 200

    json_data1 = res1.json()
    json_data2 = res2.json()

    assert json_data1["username"] == "test_user1"
    assert json_data2["username"] == "test_user2"


def test_create_coordinates_for_users():
    res = client.post("/coordinates/1", json={"latitude": 1.1, "longitude": 1.1})
    json_data = res.json()

    assert res.status_code == 200
    assert json_data["latitude"] == 1.1
    assert json_data["longitude"] == 1.1

    time.sleep(1)

    res = client.post("/coordinates/1", json={"latitude": 2.2, "longitude": 2.2})

    json_data = res.json()

    assert res.status_code == 200
    assert json_data["latitude"] == 2.2
    assert json_data["longitude"] == 2.2

    time.sleep(1)

    res = client.post("/coordinates/1", json={"latitude": 3.3, "longitude": 3.3})

    json_data = res.json()

    assert res.status_code == 200
    assert json_data["latitude"] == 3.3
    assert json_data["longitude"] == 3.3

    time.sleep(1)

    res = client.post("/coordinates/2", json={"latitude": 1.1, "longitude": 1.1})

    json_data = res.json()

    assert res.status_code == 200
    assert json_data["latitude"] == 1.1
    assert json_data["longitude"] == 1.1


def test_get_coordinates_of_user():
    res1 = client.get("/get_user/1")
    json_data1 = res1.json()

    assert res1.status_code == 200
    assert len(json_data1["coordinates"]) == 3

    res2 = client.get("/get_user/2")
    json_data = res2.json()

    assert res2.status_code == 200
    assert len(json_data["coordinates"]) == 1


def test_get_users_latest_coordinate():
    res = client.get("/get_user/1")
    json_data = res.json()

    coordinates = json_data["coordinates"]

    assert res.status_code == 200
    assert coordinates[0]["ts"] < coordinates[1]["ts"] < coordinates[2]["ts"]


def test_remove_db():
    os.remove("test.db")

    assert os.path.exists("test.db") == False
