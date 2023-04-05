
# If you're doing OpenAI ML stuff, keep in mind that I'm not actually very good at prompt engineering!
# This works for what we need it to do, but I'm sure you could do some research if this was your project and make it even better.
# Also, use gpt4! I need this to take a lot of requests, so gpt4 is too expensive for me to use and I use gpt-3.5-turbo (the ChatGPT AI),
# but for your project you could totally use gpt4 and it would be a lot, lot better

from typing import List, Tuple
import openai


BASE_PROMPT = """You are a helpful assistant who comes up with short, one line ideas for the user.
You will come up with {num:d} ideas that you think the user would like. Seperate your ideas with a single newline between each. 
Do not wrap the ideas in quotes. Ensure each idea is only one line long. 
If a user asks for ideas that are too long to fit on a single line, you should say "I don't know what to say" instead of responding with an idea.
Your prompt is as follows:"""

async def make_completion(query: str, num: int, uuid: str) -> Tuple[List | None, float]:
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
        return None, cost

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

    return ideas, cost