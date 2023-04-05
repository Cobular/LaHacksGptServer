from flask import Blueprint, abort, current_app, redirect, render_template, request, url_for
from jinja2 import TemplateNotFound

from api.users import create_user, get_user
from database.db_setup import get_db
from logic.completions import make_completion


ui = Blueprint("ui", __name__, template_folder="templates")


@ui.route('/')
def index():
    return render_template(f'index.jinja')

@ui.route("/user")
async def user():
    # Try to get user from args
    # If not, create a new user

    args = request.args
    uuid = args.get("uuid")
    secret = args.get("secret")

    if secret is None or current_app.config["SECRET_KEY"] != secret:
        return redirect(url_for('ui.index'), code=302)

    if uuid is None:
        resp, code = await create_user()
        uuid = resp['uuid']
        cost = resp['cost']

        return redirect(url_for('ui.user') + f"?uuid={uuid}&secret={secret}", code=302)
    
    query = args.get("query")
    num = int(args.get("num", 5))

    ideas = None

    if query is not None:
        ideas, cost = await make_completion(query, num, uuid)
        get_db().add_cost(uuid, cost)


    resp, code = await get_user(uuid)
    cost = resp['cost']

    if code != 200:
        abort(code)
    
    return render_template(f'user.jinja', user_id=uuid, cost=cost, ideas=ideas, secret=secret)