from utilities.db import Database


class Service:
    """Service layer for database functionality"""
    def __init__(self, database_uri: str):
        self.db = Database(database_uri)

    def get_all_coordinate_entries(self):
        """Get all coordinate entries"""
        return self.db.execute("SELECT * FROM coordinates").fetchall()
    
    def get_users_coordinates(self, user_id: int):
        """Get all coordinate entries of a user with given user_id"""
        return self.db.execute(f"SELECT * FROM coordinates WHERE user_id = {user_id}").fetchall()

    def create_coordinates(self, user_id: int, latitude: float, longitude: float):
        """Create new coordinate entry to the database for a user with given user_id"""
        return self.db.execute(f"INSERT INTO coordinates (user_id, latitude, longitude, ts) VALUES ({user_id}, {latitude}, {longitude}, now())")

    # Create a new user
    def create_user(self, username: str, passwd: str):
        """Create new user entry to the database with given parameters"""
        return self.db.execute(f"INSERT INTO users (username, passwd) VALUES ('{username}', '{passwd}')")