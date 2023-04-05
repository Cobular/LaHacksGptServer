import json
from werkzeug.exceptions import HTTPException
from flask import Blueprint, Flask
from sqlite3 import Error as SqliteError

from database.db_setup import get_db

user = Blueprint("user", __name__)


@user.route("/user", methods=["POST"])
async def create_user():
    """Create a user

    Returns:
        Response: The UUID of the user, or an error
    """
    uuid, cost = get_db().insert_user()
    return {"success": True, "uuid": uuid, "cost": cost}, 200



@user.route("/user/<uuid>", methods=["GET"])
async def get_user(uuid: str):
    """Check that a user exists

    Returns:
        Response: The UUID of the user, or an error
    """
    user = get_db().get_user(uuid)
    if user is None:
        return {"success": False, "error": "User does not exist"}, 400
    return {"success": True, "uuid": user.uuid, "cost": user.cost}, 200
