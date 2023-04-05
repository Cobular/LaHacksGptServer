from flask import Blueprint

from api.errors import register_error_handlers
from .completions import completion
from .users import user


api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(completion)
api.register_blueprint(user)
register_error_handlers(api)