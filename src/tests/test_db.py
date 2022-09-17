import unittest

import os
from dotenv import load_dotenv

from utilities.db import Database

load_dotenv()
database_uri = os.environ.get("TEST_DATABASE_URI")


class TestDatabase(unittest.TestCase):

    db = Database(database_uri)

    @classmethod
    def setUpClass(cls) -> None:
        cls.db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, passwd TEXT NOT NULL)")
        cls.db.execute("CREATE TABLE coordinates (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER REFERENCES users ON DELETE CASCADE, latitude FLOAT, longitude FLOAT, ts TIMESTAMP)")

        cls.db.execute("INSERT INTO users (username, passwd) VALUES ('Person1', 'Person1')")
        cls.db.execute("INSERT INTO users (username, passwd) VALUES ('Person2', 'Person2')")
        
        cls.db.execute("INSERT INTO coordinates (user_id, latitude, longitude, ts) VALUES (1, 1.1, 1.1, strftime('%Y-%m-%d %H:%M:%S:%f','now'))")
        cls.db.execute("INSERT INTO coordinates (user_id, latitude, longitude, ts) VALUES (1, 2.2, 2.2, strftime('%Y-%m-%d %H:%M:%S:%f','now'))")
        cls.db.execute("INSERT INTO coordinates (user_id, latitude, longitude, ts) VALUES (1, 3.3, 3.3, strftime('%Y-%m-%d %H:%M:%S:%f','now'))")
        cls.db.execute("INSERT INTO coordinates (user_id, latitude, longitude, ts) VALUES (1, 4.4, 4.4, strftime('%Y-%m-%d %H:%M:%S:%f','now'))")
        cls.db.execute("INSERT INTO coordinates (user_id, latitude, longitude, ts) VALUES (2, 5.5, 5.5, strftime('%Y-%m-%d %H:%M:%S:%f','now'))")
        cls.db.execute("INSERT INTO coordinates (user_id, latitude, longitude, ts) VALUES (2, 6.6, 6.6, strftime('%Y-%m-%d %H:%M:%S:%f','now'))")
        cls.db.execute("INSERT INTO coordinates (user_id, latitude, longitude, ts) VALUES (2, 6.6, 6.6, strftime('%Y-%m-%d %H:%M:%S:%f','now'))")

    def test_users_are_inserted(self):
        query = self.db.execute("SELECT * FROM users").fetchall()
        
        assert len(query) == 2
        assert query[0].username == "Person1"
        assert query[1].username == "Person2"
        
    def test_coordinates_are_inserted(self):
        query = self.db.execute("SELECT * FROM coordinates").fetchall()

        assert len(query) == 7

    def test_user_specific_coordinates_are_found(self):
        query = self.db.execute("SELECT * FROM coordinates WHERE user_id = 1").fetchall()
        query2 = self.db.execute("SELECT * FROM coordinates WHERE user_id = 2").fetchall()

        assert len(query) == 4
        assert len(query2) == 3

    def test_users_latest_entry_is_found(self):
        query = self.db.execute("SELECT * FROM coordinates WHERE user_id = 2 ORDER BY ts DESC").fetchall()
        
        assert query[0].ts > query[1].ts
        assert query[0].ts > query[2].ts

    def test_users_route_is_in_right_order(self):
        query = self.db.execute("SELECT * FROM coordinates WHERE user_id = 1 ORDER BY ts DESC").fetchall()

        assert query[3].latitude == 1.1
        assert query[2].latitude == 2.2
        assert query[1].latitude == 3.3
        assert query[0].latitude == 4.4

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(database_uri[10:])        

