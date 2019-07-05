#!/usr/bin/env python3

import json
import sys

# Global constants
required_json_keys = []

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

def handle(req):
    # Hash table for the deserialized request.
    arguments = {}

    # Ensure that the client sent JSON and not something else.
    arguments = deserialize_content(req)
    print(arguments)
    if not arguments:
        return("Couldn't deserialize request.")

    # Ensure the request has everything needed.
    if not ensure_all_keys(arguments):
        return("Request was missing a key.")

    # Do the actual stuff here...

if __name__ == "__main__":
    print("Unit testing mode engaged.")
    print("Trying broken request JSON.")
    broken_json = {}
    print(handle(json.dumps(broken_json)))
    print()

    print("Trying valid request JSON.")
    valid_json = {}
    print(handle(json.dumps(valid_json)))
    print()

    sys.exit(0)

