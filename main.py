import os
from flask import Flask, request
from werkzeug.local import LocalProxy

from flask import g
import openai
from aiohttp import ClientSession

from dotenv import load_dotenv

load_dotenv()


BASE_PROMPT = """You are a helpful assistant who comes up with short, one line ideas for the user.
You will come up with {num:d} ideas that you think the user would like. Seperate your ideas with a single newline between each. 
Do not wrap the ideas in quotes. Ensure each idea is only one line long. 
If a user asks for ideas that are too long to fit on a single line, you should say "I don't know what to say" instead of responding with an idea.
Your prompt is as follows:"""


app = Flask(__name__)


@app.route("/", methods=["GET"])
async def get_completion():
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

    prompt = BASE_PROMPT.format(num=num)

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ],
    )
    message = response.choices[0].message["content"]

    cost = (response["usage"]["total_tokens"] / 1000) * 0.002

    if message == "I don't know what to say":
        return {
            "success": False,
            "cost": cost,
            "error": "Generation failed to be correct. Please try again, revising your prompt. Ensure you ask for 5 or fewer ideas and that a response can fit on a single line.",
        }, 400

    # Parse the data we want from the response
    ideas = message.split("\n")
    # This is really stupid, but the model will always return the data with either prefixed
    # numbers or dashes. We need to strip those off.
    if ideas[0].startswith("- "):
        ideas = [idea[2:] for idea in ideas]
    elif ideas[0].startswith("1. "):
        ideas = [idea[3:] for idea in ideas]

    # Remove any empty strings
    ideas = [idea for idea in ideas if idea != ""]

    if len(ideas) > num:
        return {
            "success": False,
            "cost": cost,
            "error": "Generation failed to be correct, generated too long of a response. Please try again, revising your prompt. Ensure you ask for 5 or fewer ideas and that a response can fit on a single line.",
        }, 400

    return {"success": True, "completion": ideas, "cost": cost}
