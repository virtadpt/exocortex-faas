#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 :

#   A microservice that takes a JSON document POSTed to it containing an
#   arbitrary string of some kind (read: secret key) and runs an HMAC
#   (https://en.wikipedia.org/wiki/Hash-based_message_authentication_code)
#   on it.  The HMAC'd data is then returned to the client as a JSON document
#   of the form { "result": "<HMAC here>" }.  The HMAC will be base64 encoded.
#
#   This microservice also supports the generation of Javascript Web Tokens
#   (https://jwt.io/) if pyjwt (https://github.com/jpadilla/pyjwt/) is
#   installed.
#
#   The use case for this should be pretty obvious: You want to interact with
#   an API programmatically but it requires that your requests be HMAC'd for
#   security, or it requires a JWT for Bearer authentication.  Not every
#   framework has working HMAC or JWT implementations, so this offloads that
#   work and hopefully saves your sanity.
#
#   If you make a GET request to / you'll get the online docs.

# By: The Doctor <drwho at virtadpt dot net>
# License: GPLv3

# v4.0 - Turned into a function-as-a-service.
# v3.0 - Ported to Python 3.
# v2.0 - Added Javascript Web Token support (if pyjwt is installed).  This was
#        a fair amount of work, so it makes sense to bump the version number.
#      - Refactored code to break the heavy lifting out into separate helper
#        methods.  This also made it possible to add JWT support without turning
#        it into spaghetti code.
#      - Updated online help.
# v1.0 - Initial release.

# Load modules.
import base64
import hashlib
import hmac
import json
import jwt
import sys

# Global constants.
required_hmac_keys = [ "data", "hash", "secret" ]
supported_hmac_hashes = [ "md5", "sha1", "sha224", "sha256", "sha384", "sha512" ]

required_jwt_keys = [ "hash", "headers", "payload", "secret" ]
supported_jwt_algorithms = [ "HS256", "HS384", "HS512" ]

# Try to deserialize content from the client.  Return the hash table
# containing the deserialized JSON if it exists.
def deserialize_content(content):
    arguments = {}
    try:
        arguments = json.loads(content)
    except:
        return None
    return arguments

# Ensure that all of the keys required to generate a Javascript Web Token
# are in the hash table.
def ensure_all_jwt_keys(arguments):
    all_keys_found = True
    for key in required_jwt_keys:
        if key not in list(arguments.keys()):
            all_keys_found = False
    if not all_keys_found:
        return False
    else:
        return True

# Helper method that does the heavy lifting of generating Javascript Web
# tokens.
def generate_jwt(arguments):
    jwt_token = None

    # Ensure that all of the required keys are in the JSON document.
    if not ensure_all_jwt_keys(arguments):
        return "Your request was missing some keys.  You need to have: " + str(required_jwt_keys)

    # Generate a JWT.
    jwt_token = jwt.encode(arguments["payload"], arguments["secret"],
        arguments["headers"]["alg"])

    # Return the JWT to the client.
    return jwt_token.decode("utf-8")

# Ensure that all of the keys required to carry out an HMAC are in the
# hash table.
def ensure_all_hmac_keys(arguments):
    all_keys_found = True
    for key in required_hmac_keys:
        if key not in list(arguments.keys()):
            all_keys_found = False
    if not all_keys_found:
        return False
    else:
        return True

# Helper method that does the heavy lifting of generating HMACs of data.
def generate_hmac(arguments):
    hasher = None

    # Ensure that all of the required keys are in the JSON document.
    if not ensure_all_hmac_keys(arguments):
        return "Your request was missing some keys.  You need to have: " + str(required_hmac_keys)

    # Determine which hash to use with the HMAC and run it on the data.
    if arguments["hash"] == "md5":
        hasher = hmac.new(bytes(arguments["secret"], "utf-8"),
            bytes(arguments["data"], "utf-8"), hashlib.md5)
    if arguments["hash"] == "sha1":
        hasher = hmac.new(bytes(arguments["secret"], "utf-8"),
            bytes(arguments["data"], "utf-8"), hashlib.sha1)
    if arguments["hash"] == "sha224":
        hasher = hmac.new(bytes(arguments["secret"], "utf-8"),
            bytes(arguments["data"], "utf-8"), hashlib.sha224)
    if arguments["hash"] == "sha256":
        hasher = hmac.new(bytes(arguments["secret"], "utf-8"),
            bytes(arguments["data"], "utf-8"), hashlib.sha256)
    if arguments["hash"] == "sha384":
        hasher = hmac.new(bytes(arguments["secret"], "utf-8"),
            bytes(arguments["data"], "utf-8"), hashlib.sha384)
    if arguments["hash"] == "sha512":
        hasher = hmac.new(bytes(arguments["secret"], "utf-8"),
            bytes(arguments["data"], "utf-8"), hashlib.sha512)

    return(hasher.hexdigest())

# Handle the request.
def handle(request):
    token = None
    arguments = {}

    # Handle the case where the request is empty.
    if not request:
        return "Where was the request?"

    # Ensure that the client sent JSON and not something else.
    arguments = deserialize_content(request)
    if not arguments:
        return "Couldn't deserialize request."

    # Determine if we should generate a JWT or an HMAC using the
    # appropriate helper method.
    if arguments["hash"] == "jwt":
        token = generate_jwt(arguments)
    else:
        token = generate_hmac(arguments)
    return token

if __name__ == "__main__":
    print("Unit testing mode enabled.")
    print("Testing HMACs.")

    # Hardcode some test vectors generated separately.
    hmac_test_vectors = {}
    hmac_test_vectors ["md5"] = "df08aef118f36b32e29d2f47cda649b6"
    hmac_test_vectors ["sha1"] = "i9818e3306ba5ac267b5f2679fe4abd37e6cd7b54"
    hmac_test_vectors ["sha224"] = "cf60fd8a83892d5e0ab0ee6efe94d11c514fa478fc97413c37a765c5"
    hmac_test_vectors ["sha256"] = "1b2c16b75bd2a870c114153ccda5bcfca63314bc722fa160d690de133ccbb9db"
    hmac_test_vectors ["sha384"] = "d7d15057b821cfc2f9f0e3e8f8fc093c5f661c4c9215f1d0dfddf6effd547fd6d1587fa8577a553cc49b0e257313ac52"
    hmac_test_vectors ["sha512"] = "6274071d33dec2728a2a1c903697fc1210b3252221c3d137e12d9f1ae5c8ed53e05e692b05a9eefff289667e2387c0fc0bd8a3d9bd7000782730c856a77a77d5"

    # Set up the arguments hash.
    arguments = {}
    arguments["data"] = "data"
    arguments["secret"] = "secret"

    # Capture the output.
    output = ""

    # Roll through the supported hashes and compare their outputs to our
    # test vectors.
    for i in supported_hmac_hashes:
        print("Testing hash " + i + ".")
        arguments["hash"] = i
        print("Value of arguments: " + str(arguments))
        output = handle(json.dumps(arguments))
        print("Value of output: " + output)
        if output == hmac_test_vectors[i]:
            print("HMAC " + i + " checks out.")
        else:
            print("HMAC " + i + " failed.")
        print()

    print("Testing JWTs.")

    # Hardcode some test vectors generated separately.
    jwt_test_vectors = {}
    jwt_test_vectors["HS256"] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmb28iOiJiYXIiLCJiYXoiOiJxdXV4In0.NvrvToUN9NqZXOtXoowxzr_MJPwBucT-R8t9mlBdulw"
    jwt_test_vectors["HS384"] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9.eyJmb28iOiJiYXIiLCJiYXoiOiJxdXV4In0.NYTwQz44NdyPZrIk9khXkyD-cmCy03jdausztGVimwX34e_aVTvvqVIJd1F3yr3G"
    jwt_test_vectors["HS512"] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJmb28iOiJiYXIiLCJiYXoiOiJxdXV4In0.3PFRw_Hl4JDJULFU_j_aWgm4YvH9R5KGtGq0T4_pTiONbRsUd4QkrktfIMsPivbz9P0lCxfjp0G5USNcC4cocA"

    # Set up the arguments hash.
    arguments = {}
    arguments["hash"] = "jwt"
    arguments["headers"] = {}
    arguments["headers"]["typ"] = "JWT"
    arguments["headers"]["alg"] = ""
    arguments["payload"] = {}
    arguments["payload"]["foo"] = "bar"
    arguments["payload"]["baz"] = "quux"
    arguments["secret"] = "secret"

    # Capture the output.
    output = ""

    for i in supported_jwt_algorithms:
        print("Testing JWT algorithm " + i + ".")
        arguments["headers"]["alg"] = i
        print("Value of arguments: " + str(arguments))
        output = handle(json.dumps(arguments))
        print("Value of output: " + str(output))
        if output == jwt_test_vectors[i]:
            print("JWT " + i + " checks out.")
        else:
            print("JWT " + i + " failed.")
        print()

    print("End of unit tests.")
    sys.exit(0)
