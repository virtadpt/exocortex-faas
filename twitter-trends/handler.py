#!/usr/bin/env python3

import json
import sys

from twitter import *

# Global constants
required_json_keys = [ "access_key", "access_secret", "consumer_key",
    "consumer_secret", "location_id" ]

help = """
"""

# Try to deserialize content from the client.  Return the hash table
# containing the deserialized JSON if it exists.
def deserialize_content(content):
    arguments = {}
    try:
        arguments = json.loads(content)
    except:
        return None
    return arguments

# Ensure that all of the keys required are in the hash table.
def ensure_all_keys(arguments):
    all_keys_found = True
    for key in required_json_keys:
        if key not in list(arguments.keys()):
            all_keys_found = False
    if not all_keys_found:
        return False
    else:
        return True

# Core code of the function.
# Args:
#   req (str): Serialized JSON containing the Twitter Trends API request.
#       {
#           "access_key": "",
#           "access_secret": "",
#           "consumer_key": "",
#           "consumer_secret": "",
#           "location_id": ""
#       }
def handle(req):
    # Hash table for the deserialized request.
    arguments = {}

    # Handle to a Twitter API connection.
    twitter = None

    # Hash table containing trending information from Twitter.
    trends = {}

    # Ensure that the client sent JSON and not something else.
    arguments = deserialize_content(req)
    print(arguments)
    if not arguments:
        return("Couldn't deserialize request.")

    # Ensure the request has everything needed.
    if not ensure_all_keys(arguments):
        return("Request was missing a key.")

    # Set up a Twitter API connection.
    twitter = Twitter(auth=OAuth(arguments["access_key"],
        arguments["access_secret"], arguments["consumer_key"],
        arguments["consumer_secret"]))
    if not twitter:
        return("Twitter API connection failed.")

    # Pull trending information from the Twitter API.
    trends = twitter.trends.place(_id=arguments["location_id"])
    return(trends)

if __name__ == "__main__":
    print("Unit testing mode engaged.")
    print("Trying broken request JSON.")
    broken_json = {}
    broken_json["access_key"] = "12345"
    broken_json["access_secret"] = "abcde"
    broken_json["consumer_key"] = "67890"
    print(handle(json.dumps(broken_json)))
    print()

    print("Trying valid request JSON.")
    valid_json = {}
    valid_json["access_key"] = "12345"
    valid_json["access_secret"] = "abcde"
    valid_json["consumer_key"] = "67890"
    valid_json["consumer_secret"] = "vwxyz"
    valid_json["location_id"] = "31337"
    print(handle(json.dumps(valid_json)))
    print()

    sys.exit(0)

