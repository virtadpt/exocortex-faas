#!/usr/bin/env python3

import random
import sys

responses = [
    "Sounds like an injury counter reset to me.",
    "How many fingers do you need to do magic?",
    "Just because it's in the name of science doesn't mean it's a good idea.",
    "You're only doing this because you saw it in a movie, aren't you?",
    "Don't forget the fire extinguisher.",
    "You're gonna want more than eye protection for that one.",
    "I need the dexterity."
    ]

def handle(req):
    response = random.choice(responses)
    return response

if __name__ == "__main__":
    print(handle(None))
    sys.exit(0)
