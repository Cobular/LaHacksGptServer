import sqlite3
from typing import NamedTuple
from uuid import uuid4
import sqlite3

import click
from flask import current_app, g

from database.db_manager import DbManager


def get_db() -> DbManager:
    """Create the flask database context"""
    if "db" not in g:
        g.db = DbManager(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)

    return g.db


def close_db(e=None):
    """Cleanup the flask database context"""
    db = g.pop("db", None)

    if db is not None:
        del db


def init_db():
    """Wipe and recreate the database"""
    db = get_db()

    with current_app.open_resource("database/schema.sql") as f:
        db.conn.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Call from the app factory to register the database"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

