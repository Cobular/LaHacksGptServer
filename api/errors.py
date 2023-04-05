from http.client import HTTPException
import json
from sqlite3 import Error

from flask import Flask


def handle_generic_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "success": False,
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


def handle_sqlite_exception(e: Error):
    return {"success": False, "error": str(e)}, 500


def register_error_handlers(app: Flask):
    app.register_error_handler(HTTPException, handle_generic_exception)
    app.register_error_handler(Error, handle_sqlite_exception)
