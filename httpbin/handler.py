#!/usr/bin/env python3

import json
import requests
import sys

def handle(req):
    # List of responses from httpbin.org
    responses = []

    url = "https://httpbin.org"
    request = requests.get(url+"/get")
    responses.append(request.json())

    request = requests.get(url+"/headers")
    responses.append(request.json())

    request = requests.get(url+"/ip")
    responses.append(request.json())

    request = requests.get(url+"/user-agent")
    responses.append(request.json())

    request = requests.get(url+"/uuid")
    responses.append(request.json())

    return responses

if __name__ == "__main__":
    print("Running in unit testing mode!")
    output = handle("Test text.")
    for i in output:
        print(json.dumps(i, indent=4, sort_keys=True))
    sys.exit(0)
