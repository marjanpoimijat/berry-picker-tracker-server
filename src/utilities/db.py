from enum import unique
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey
import sqlalchemy


class Database:
    def __init__(self, database_uri: str):
        """Connect to a database with given database URI"""
        try:
            self.engine = create_engine(database_uri)

            metadata_obj = MetaData()

            user = Table('users', metadata_obj,
            Column('user_id', Integer, primary_key=True),
            Column('username', String,  unique=True, nullable=False),
            Column('passwd', String, nullable=False)
            )

            coordinate = Table('coordinates', metadata_obj,
                Column('id', Integer, primary_key=True),
                Column('user_id', Integer, ForeignKey('users.user_id'), nullable = False),
                Column('latitude', Float, nullable=False),
                Column('longitude', Float, nullable=False),
                Column('ts', DateTime(timezone=True), server_default=func.now()))

            metadata_obj.create_all(self.engine, checkfirst=True)
            self.connection = self.engine.connect()
        except Exception as e:
            print(e)

    def execute(self, statement: str):
        """Call to execute any SQL statement"""
        try:
            return self.connection.execute(statement)
        except Exception as e:
            print(e)