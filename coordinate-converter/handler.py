#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 :

# by: The Doctor [412/724/301/703/415/510] <drwho at virtadpt dot net>

# v2.0 - Refactored so it's significantly neater and easier to maintain.
# v1.0 - Initial release.

import json
import mgrs
import re
import sys

# These get swapped depending on if I'm debugging or running under OpenFaaS.
# Local.
from .openlocationcode import *
# OpenFaas.
#from openlocationcode import *

help = """
This is a microservice which turns one set of map coordinates into another.

Takes as its input a JSON document of the form:
    {
        "coordinates": "<the coordinates to convert>",
        "from": "<type of the coordinates to convert>",
        "to": "<type to convert the coordinates to>"
    }

Supported coordinate types:
* degrees/minutes/seconds (dms)
** 48°53'10.18"N 2°20'35.09"E
* decimal degrees (dd)
** -48.8866111111 -2.34330555556
* open location code (openlocationcode, pluscode)
** 8FVC9G8F+6X
* Military Grid Reference System (mgrs)
** 4QFJ1234567890

If you supply the wrong kind of coordinates for the type given, you will get bad results.
"""
required_keys = [ "coordinates", "from", "to" ]
supported_coordinates = [ "dms", "dd", "openlocationcode", "pluscode", "mgrs" ]

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
    for key in required_keys:
        if key not in list(arguments.keys()):
            all_keys_found = False
    if not all_keys_found:
        return False
    else:
        return True

# Converts degrees/minutes/seconds to decimal degrees.  Takes one set of d/m/s at a time
#   (i.e., latitude only, longitude only).
def dms_to_dd(coordinate):
    sign = None
    degrees = 0
    minutes = 0
    seconds = 0
    fraction_of_a_second = 0
    dd = None

    # North and east are positive, south and west are negative.
    if re.search("[neNE]", coordinate):
        sign = 1.0
    else:
        sign = -1.0

    # Chop the coordinates up into a list of numerical values by dropping everything that
    # isn't a numerical value.  We do a double conversion because of how Python 3 implements
    # filter() now.  It'll look something like this: [48, 53, 10, 18]
    coordinate = filter(len, re.split("\D+", coordinate, maxsplit=4))
    coordinate = list(coordinate)

    # Degrees.
    degrees = int(coordinate[0])

    # Minutes.
    if len(coordinate) >= 2:
        minutes = int(coordinate[1])

    # Seconds.
    if len(coordinate) >= 3:
        seconds = int(coordinate[2])

    # Fractions of a second.
    if len(coordinate) >= 4:
        fraction_of_a_second = int(coordinate[3])

    # Collapse the two into fractional seconds.
    seconds = str(seconds) + "." + str(fraction_of_a_second)
    seconds = float(seconds)

    # Turn it into a decimal degree coordinate.
    dd = sign * (float(degrees) + float(minutes / 60) + float(seconds / 3600))

    return(dd)

# Converts decimal degrees to degrees/minutes/seconds.  Takes one coordinate at a time.
def dd_to_dms(coordinate):
    degrees = 0
    minutes = 0
    seconds = 0
    sign = ""
    dms = ""

    # Split apart the decimal value.
    coordinate = float(coordinate)
    (minutes, seconds) = divmod((coordinate * 3600), 60)
    (degrees, minutes) = divmod(minutes, 60)

    # Save the sign so we can figure out north/south/east/west afterward.
    if degrees < 0.0:
        degrees = degrees * -1
        sign = "-"
    else:
        sign = "+"

    # Assemble the coordinate string.
    dms = str(degrees) + "° " + str(minutes) + "' " + str(seconds) + "\" " + sign

    return(dms)

# Converts a set of decimal degree coordinates into a pluscode.  Takes as its argument
#   a string containing both the latitude and longitude as strings.
def dd_to_pluscode(coordinates):
    latitude = 0.0
    longitude = 0.0
    pluscode = ""

    # Extract the latitude and longitude.
    (latitude, longitude) = coordinates.split()
    latitude = float(latitude)
    longitude = float(longitude)

    # Do the thing.
    pluscode = encode(latitude, longitude)

    return(pluscode)

# Converts an open location code into decimal degree coordinates.  Takes as its argument a
#   string containing a pluscode.  Returns latitude and longitude.
def pluscode_to_dd(pluscode):
    codearea = None
    latitude = 0.0
    longitude = 00

    codearea = decode(pluscode)
    latitude = codearea.latitudeCenter
    longitude = codearea.longitudeCenter

    return(str(latitude) + " " + str(longitude))

# Convert dd to mgrs.  Returns a string with the gridref.
def dd_to_mgrs(latitude, longitude):
    gridref = None

    converter = mgrs.MGRS()
    gridref = converter.toMGRS(latitude, longitude)

    return(gridref)

# Convert mgrs to dd.  Returns a string with the latitude and longitude.
def mgrs_to_dd(gridref):
    coordinates = None

    converter = mgrs.MGRS()
    gridref = str.encode(gridref)
    coordinates = converter.toLatLon(gridref)
    coordinates = str(coordinates[0]) + " " + str(coordinates[1]) 

    return(coordinates)

# Entry point to the function.
def handle(req):
    coordinates = {}
    latitude = None
    longitude = None
    pluscode = None
    gridref = None

    # If no input, return online help.
    if not req:
        return(help)

    # Deserialize the JSON document from the user.
    coordinates = deserialize_content(req)
    if not coordinates:
        return("Could not deserialize JSON.")

    # Make sure we have everything we need.
    if not ensure_all_keys(coordinates):
        return("Required key missing in JSON.")

    # Make sure the types of the supplied coordinates is supported.
    if coordinates["from"] not in supported_coordinates:
        return("I don't support that input coordinate type.")
    if coordinates["to"] not in supported_coordinates:
        return("I don't support that output coordinate type.")

    # Case: dms to something
    if (coordinates["from"] == "dms"):

        # Case: output is dd.
        if (coordinates["to"] == "dd"):
            (latitude, longitude) = coordinates["coordinates"].split()
            latitude = str(dms_to_dd(latitude))
            longitude = str(dms_to_dd(longitude))
            return(latitude + " " + longitude)

        # Case: output is openlocationcode/pluscode.
        if (coordinates["to"] == "openlocationcode") or (coordinates["to"] == "pluscode"):

            # First convert to dd.
            (latitude, longitude) = coordinates["coordinates"].split()
            latitude = str(dms_to_dd(latitude))
            longitude = str(dms_to_dd(longitude))

            # Pass dd to the pluscode generator.
            pluscode = dd_to_pluscode(latitude + " " + longitude)
            return(pluscode)

        # Case: output is mgrs.
        if (coordinates["to"] == "mgrs"):

            # First convert to dd.
            (latitude, longitude) = coordinates["coordinates"].split()
            latitude = str(dms_to_dd(latitude))
            longitude = str(dms_to_dd(longitude))

            # Pass dd to the mgrs generator.
            gridref = dd_to_mgrs(latitude, longitude)
            return(gridref)





    # Case: dd to something
    if (coordinates["from"] == "dd"):

        # Case: output is dms.
        if (coordinates["to"] == "dms"):
            (latitude, longitude) = coordinates["coordinates"].split()

            latitude = dd_to_dms(latitude)
            if "+" in latitude:
                latitude = re.sub("\+", "N", latitude)
            else:
                latitude = re.sub("\-", "S", latitude)

            longitude = dd_to_dms(longitude)
            if "+" in longitude:
                longitude = re.sub("\+", "E", longitude)
            else:
                longitude = re.sub("\-", "W", longitude)

            return(latitude + " " + longitude)

        # Case: output is openlocationcode/pluscode.
        if (coordinates["to"] == "openlocationcode") or (coordinates["to"] == "pluscode"):
            pluscode = dd_to_pluscode(coordinates["coordinates"])
            return(pluscode)

        # Case: output is mgrs.
        if (coordinates["to"] == "mgrs"):
            (latitude, longitude) = coordinates["coordinates"].split()
            gridref = dd_to_mgrs(latitude, longitude)
            return(gridref)




    # Case: openlocationcode/pluscode to something.
    if (coordinates["from"] == "openlocationcode") or (coordinates["from"] == "pluscode"):

        # Case: output is dd.
        if coordinates["to"] == "dd":
            coordinates = pluscode_to_dd(coordinates["coordinates"])
            (latitude, longitude) = coordinates.split()
            return(latitude + " " + longitude)

        # Case: output is dms.
        if coordinates["to"] == "dms":

            # First convert to dd.
            coordinates = pluscode_to_dd(coordinates["coordinates"])
            (latitude, longitude) = coordinates.split()

            # Now convert dd to dms.
            latitude = dd_to_dms(latitude)
            if "+" in latitude:
                latitude = re.sub("\+", "N", latitude)
            else:
                latitude = re.sub("\-", "S", latitude)

            longitude = dd_to_dms(longitude)
            if "+" in longitude:
                longitude = re.sub("\+", "E", longitude)
            else:
                longitude = re.sub("\-", "W", longitude)
            return(latitude + " " + longitude)

        # Case: output is mgrs.
        if coordinates["to"] == "mgrs":

            # First convert to dd.
            coordinates = pluscode_to_dd(coordinates["coordinates"])
            (latitude, longitude) = coordinates.split()

            # Pass dd to the mgrs generator.
            gridref = dd_to_mgrs(latitude, longitude)
            return(gridref)




    # Case: mgrs to something.
    if (coordinates["from"] == "mgrs"):

        # Case: output is dd.
        if coordinates["to"] == "dd":
            coordinates = mgrs_to_dd(coordinates["coordinates"])
            return(coordinates)

        # Case: output is dms.
        if coordinates["to"] == "dms":

            # First convert to dd.
            coordinates = mgrs_to_dd(coordinates["coordinates"])
            (latitude, longitude) = coordinates.split()

            # Now convert dd to dms.
            latitude = dd_to_dms(latitude)
            if "+" in latitude:
                latitude = re.sub("\+", "N", latitude)
            else:
                latitude = re.sub("\-", "S", latitude)

            longitude = dd_to_dms(longitude)
            if "+" in longitude:
                longitude = re.sub("\+", "E", longitude)
            else:
                longitude = re.sub("\-", "W", longitude)

            return(latitude + " " + longitude)

        # Case: output is openlocationcode/pluscode.
        if (coordinates["to"] == "openlocationcode") or (coordinates["to"] == "pluscode"):

            # First convert to dd.
            coordinates = mgrs_to_dd(coordinates["coordinates"])

            # Pass dd to the pluscode generator.
            pluscode = dd_to_pluscode(coordinates)
            return(pluscode)

    return(help)

if __name__ == "__main__":
    print("Unit testing mode.")
    print("Testing bad JSON...", end=" ")
    print(handle({}))

    print("Testing missing keys detection...", end=" ")
    test = {}
    test["coordinates"] = ""
    test["from"] = ""
    print(handle(json.dumps(test)))

    print("Testing all keys can be found...", end=" ")
    test["to"] = ""
    if not handle(json.dumps(test)):
        print("All keys found.")
    else:
        print("All keys not found.  Oops.")

    print("Testing valid input coordinate type...", end=" ")
    test["from"] = "dms"
    if not handle(json.dumps(test)):
        print("'dms' supported.")
    else:
        print("'dms' not supported.  Huh.")

    print("Testing invalid input coordinate type...", end=" ")
    test["from"] = "barf"
    if not handle(json.dumps(test)):
        print("'barf' supported.")
    else:
        print("'barf' not supported.  Good.")

    print("Testing valid output coordinate type...", end=" ")
    test["coordinates"] = "48° 48°"
    test["from"] = "dms"
    test["to"] = "dd"
    if not handle(json.dumps(test)):
        print("'dd' supported.")
    else:
        print("'dd' not supported.  Huh.")

    print("Testing invalid output coordinate type...", end=" ")
    test["coordinates"] = "48° 48°"
    test["from"] = "dms"
    test["to"] = "barf"
    if not handle(json.dumps(test)):
        print("'barf' supported.")
    else:
        print("'barf' not supported.  Good.")

    # DMS conversions.
    # Test dms to dd.
    print("Converting DMS to DD...", end=" ")
    test["coordinates"] = "48°53'10.18\"N 2°20'35.09\"E"
    test["from"] = "dms"
    test["to"] = "dd"
    print(handle(json.dumps(test)))

    # Test dms to openlocationcode.
    print("Converting DMS to pluscode...", end=" ")
    test["coordinates"] = "48°53'10.18\"N 2°20'35.09\"E"
    test["from"] = "dms"
    test["to"] = "pluscode"
    print(handle(json.dumps(test)))

    # Test dms to mgrs.
    print("Converting DMS to MGRS...", end=" ")
    test["coordinates"] = "48°53'10.18\"N 2°20'35.09\"E"
    test["from"] = "dms"
    test["to"] = "mgrs"
    print(handle(json.dumps(test)))

    # DD conversions.
    # Test dd to dms.
    print("Converting DD to DMS...", end=" ")
    test["coordinates"] = "-48.8866111111 -2.34330555556"
    test["from"] = "dd"
    test["to"] = "dms"
    print(handle(json.dumps(test)))

    # Test dd to openlocation code.
    print("Converting DD to pluscode...", end=" ")
    test["coordinates"] = "-48.8866111111 -2.34330555556"
    test["from"] = "dd"
    test["to"] = "pluscode"
    print(handle(json.dumps(test)))

    # Test dd to mgrs.
    print("Converting DD to pluscode...", end=" ")
    test["coordinates"] = "-48.8866111111 -2.34330555556"
    test["from"] = "dd"
    test["to"] = "mgrs"
    print(handle(json.dumps(test)))

    # Open Location Code conversions.
    # Test converting pluscode to dd.
    print("Converting pluscode to DD...", end=" ")
    test["coordinates"] = "8FVC9G8F+6X"
    test["from"] = "pluscode"
    test["to"] = "dd"
    print(handle(json.dumps(test)))

    # Test converting pluscode to dms.
    print("Converting pluscode to DMS...", end=" ")
    test["coordinates"] = "8FVC9G8F+6X"
    test["from"] = "pluscode"
    test["to"] = "dms"
    print(handle(json.dumps(test)))

    # Test converting dd to mgrs.
    print("Converting DD to MGRS...", end=" ")
    test["coordinates"] = "-48.8866111111 -2.34330555556"
    test["from"] = "dd"
    test["to"] = "mgrs"
    print(handle(json.dumps(test)))

    # MGRS conversions.
    # Test converting mgrs to dd.
    print("Converting MGRS to DD...", end=" ")
    test["coordinates"] = "15TWG0000049776"
    test["from"] = "mgrs"
    test["to"] = "dd"
    print(handle(json.dumps(test)))

    # Test converting mgrs to dms.
    print("Converting MGRS to DMS...", end=" ")
    test["coordinates"] = "15TWG0000049776"
    test["from"] = "mgrs"
    test["to"] = "dms"
    print(handle(json.dumps(test)))

    # Test converting mgrs to pluscode.
    print("Converting MGRS to Open Location Codes...", end=" ")
    test["coordinates"] = "15TWG0000049776"
    test["from"] = "mgrs"
    test["to"] = "openlocationcode"
    print(handle(json.dumps(test)))

    print("End of unit tests.")
    sys.exit(0)

