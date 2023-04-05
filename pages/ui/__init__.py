from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound


ui = Blueprint("ui", __name__, template_folder="templates", static_folder='static')


@ui.route('/', defaults={'page': 'index'})
@ui.route('/<page>')
def show(page):
    try:
        return render_template(f'{page}.html')
    except TemplateNotFound:
        abort(404)
        