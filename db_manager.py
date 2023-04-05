import sqlite3
from sqlite3 import Error
from typing import NamedTuple
from uuid import uuid4

class UserData(NamedTuple):
    id: int
    uuid: str
    cost: float


class DbManager():
    def __init__(self, db_file="./db.db") -> None:
          self.conn = sqlite3.connect(db_file, check_same_thread=False)

    def create_tables(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,uuid TEXT NOT NULL,cost REAL NOT NULL)""")
        
    def insert_user(self, uuid = None, cost = 0) -> str:
        if uuid is None:
            uuid = str(uuid4())
        resp = self.conn.execute(f"INSERT INTO users (uuid, cost) VALUES (:uuid, :cost)", {"uuid": uuid, "cost": cost})
        print(resp)
        return uuid
    
    def get_user(self, uuid: str) -> dict | None:
        cursor = self.conn.execute(f"SELECT * FROM users WHERE uuid = :uuid", {"uuid": uuid})

        user = cursor.fetchone()

        if user is None:
            return None

        id, uuid, cost = user

        return UserData(id, uuid, cost)
    
    def user_exists(self, uuid: str) -> bool:
        cursor = self.conn.execute(f"SELECT * FROM users WHERE uuid = :uuid", {"uuid": uuid})
        return cursor.fetchone() is not None
    
    def add_cost(self, uuid: str, cost: float) -> None:
        self.conn.execute(f"UPDATE users SET cost = cost + :cost WHERE uuid = :uuid", {"uuid": uuid, "cost": cost})
  
    def __del__(self) -> None:
        self.conn.close()