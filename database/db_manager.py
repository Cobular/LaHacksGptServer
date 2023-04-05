import sqlite3
from typing import NamedTuple
from uuid import uuid4


class UserData(NamedTuple):
    id: int
    uuid: str
    cost: float


class DbManager:
    """Database manager for the app"""

    def __init__(self, db_file="./db.db", **kwargs) -> None:
        """Create a new database manager

        Args:
            db_file (str, optional): The path to the database file. Defaults to "./db.db".
        """
        self.conn = sqlite3.connect(db_file, check_same_thread=False, **kwargs)
        self.conn.row_factory = sqlite3.Row

    def insert_user(self, uuid=None, cost=0) -> str:
        """Add a new user to the database

        Args:
            uuid (str, optional): The UUID of the user to create. Defaults to None.
            cost (int, optional): The cost to start the user at. Defaults to 0.

        Returns:
            str: The created UUID
        """
        if uuid is None:
            uuid = str(uuid4())
        resp = self.conn.execute(
            f"INSERT INTO users (uuid, cost) VALUES (:uuid, :cost)",
            {"uuid": uuid, "cost": cost},
        )
        self.conn.commit()
        return uuid

    def get_user(self, uuid: str) -> dict | None:
        """Get a user from the database

        Args:
            uuid (str, optional): The UUID of the user to find

        Returns:
            dict | None: A plain dict of the user data, or None if not found
        """

        cursor = self.conn.execute(
            f"SELECT * FROM users WHERE uuid = :uuid", {"uuid": uuid}
        )

        user = cursor.fetchone()

        if user is None:
            return None

        id, uuid, cost = user

        return UserData(id, uuid, cost)

    def user_exists(self, uuid: str) -> bool:
        """Check if a user exists in the database

        Args:
            uuid (str): The user's UUID to query

        Returns:
            bool: If the user exists
        """
        cursor = self.conn.execute(
            f"SELECT * FROM users WHERE uuid = :uuid", {"uuid": uuid}
        )
        return cursor.fetchone() is not None

    def add_cost(self, uuid: str, cost: float) -> None:
        """Add some cost to a user

        Args:
            uuid (str): The user's UUID to add cost to
            cost (float): The cost to add
        """
        self.conn.execute(
            f"UPDATE users SET cost = cost + :cost WHERE uuid = :uuid",
            {"uuid": uuid, "cost": cost},
        )
        self.conn.commit()

    def __del__(self) -> None:
        self.conn.close()
