from flask import Blueprint, request
import openai

from database.db_setup import get_db
from logic.completions import make_completion


completion = Blueprint("api/completion", __name__)


@completion.route("/completion/<uuid>", methods=["GET"])
async def get_completion(uuid: str):
    """Use GPT-3.5-turbo (ChatGPT) to complete a prompt

    Args:
        uuid (str): _description_

    Returns:
        _type_: _description_
    """
    args = request.args

    query = args.get("query")
    num = args.get("num", 5)

    if query is None:
        return {
            "success": False,
            "error": "Please provide a query as the query parameter `query`",
        }, 400

    if num > 5:
        return {
            "success": False,
            "error": "You can only request up to 5 ideas at a time",
        }, 400

    if not get_db().user_exists(uuid):
        return {
            "success": False,
            "error": "User does not exist",
        }, 400

    ideas, cost = make_completion(query, num, uuid)

    get_db().add_cost(uuid, cost)

    if ideas is None:
        return {
            "success": False,
            "cost": cost,
            "error": "Generation failed to be correct. Please try again, revising your prompt. Ensure you ask for 5 or fewer ideas and that a response can fit on a single line.",
        }, 400


    if len(ideas) > num:
        return {
            "success": False,
            "cost": cost,
            "error": "Generation failed to be correct, generated too long of a response. Please try again, revising your prompt. Ensure you ask for 5 or fewer ideas and that a response can fit on a single line.",
        }, 400

    return {"success": True, "completion": ideas, "cost": cost}
