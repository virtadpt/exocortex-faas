# This is a simple little magic 8 ball function, inspired by The Modern Rogue
# Discord server.

import random

responses = [
    "Sounds like an injury counter reset to me.",
    "How many fingers do you need to do magic?",
    "Just because it's in the name of science doesn't mean it's a good idea.",
    "You're only doing this because you saw it in a movie, aren't you?",
    "Don't forget the fire extinguisher.",
    "You're gonna want more than eye protection for that one.",
    "I need the dexterity.",
    "Why is it that whenever we hang out I find myself in a hazmat suit?",
    "I grabbed these weeds from a local area.",
    "Imagine these in the hands of someone who knows what they're doing!",
    "That looks safe.",
    "All those years of _Duck Hunt_ finally paid off!",
    "Yarrrr, there be explosions in here...."
    ]

def handle(event, context):
    response = random.choice(responses)

    response_body = {}
    response_body["statusCode"] = 200
    response_body["body"] = response

    return(response_body)
