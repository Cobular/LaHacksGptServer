import os
from flask import Flask
from flask import g

from dotenv import load_dotenv

from database.db_setup import init_app
from pages.ui import ui
from pages.errors import register_error_handlers
from pages.completions import completion
from pages.users import user
from utils import list_routes

load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'lahacks_db.sqlite'),
        SERVER_NAME=os.getenv("SERVER_NAME", "127.0.0.1:5000"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_app(app)
    register_error_handlers(app)

    app.register_blueprint(completion)
    app.register_blueprint(user)
    app.register_blueprint(ui)

    with app.app_context():
        list_routes(app)

    return app


