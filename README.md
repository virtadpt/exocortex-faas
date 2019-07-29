# exocortex-faas
Since discovering [OpenFaaS](https://www.openfaas.com/) I've been writing more and more special code for use with my [Huginn](https://github.com/huginn/huginn) installation.  It's surprisingly easy to set up and get running, and it makes it very easy to use some of the more specialized (usually, service-specific) modules for many programming languages as tools.  So, here are the FaaS (Function-as-a-Service) modules that I've been using.

Unless otherwise stated, if you make an HTTP(S) request to one of these functions without any arguments, you will get the online help.

## [8ball-tmr/](8ball-tmr/)
A magick 8-ball of quotes from the [Modern Rogue](https://www.themodernrogue.com/) Discord server.  Every time you make a GET request, it returns another quote.

### Building and deploying
* `faas-cli build -f 8ball-tmr.yml`
* `faas-cli deploy -f 8ball-tmr.yml --gateway https://your.openfaas.gateway.here:8080/`

## [calculator/](calculator/)
A simple calculator.  Send it a math problem in a request and it'll solve it.  Operators and operands have to have spaces in between them, like this:

`23 * 5`
`16 + 18 / 2`

Functions supported:
* + - * /
* fmod - modulus (floating point output)
* abs - absolute value
* ceil - ceiling
* fabs - absolute value (floating point)

### Building and deploying
* `faas-cli build -f calculator.yml`
* `faas-cli deploy -f calculator.yml --gateway https://your.openfaas.gateway.here:8080/`

## [coordinate-converter/](coordinate-converter/)
This function takes map coordinates in one of the following formats and converts them into map coordinates in any of the other formats it supports:

* degrees/minutes/seconds (dms)
** 48°53'10.18"N 2°20'35.09"E
* decimal degrees (dd)
** -48.8866111111 -2.34330555556
* [open location code](https://plus.codes/) (openlocationcode, pluscode)
** 8FVC9G8F+6X
* [Military Grid Reference System](https://en.wikipedia.org/wiki/Military_Grid_Reference_System) (mgrs)
** 4QFJ1234567890

Inputs should look like this:

```
{
  "coordinates": "<the coordinates to convert>",
  "from": "<type of the coordinates to convert>",
  "to": "<type to convert the coordinates to>"
}
```

### Building and deploying
Due to the fact that one of the dependent modules is a wrapper around a C library, some additional flags need to be passed to `faas-cli` when building the container:

* `faas-cli build -f coordinate-converter.yml  -b ADDITIONAL_PACKAGE="gcc libc-dev"`
* `faas-cli deploy -f coordinate-converter.yml --gateway https://your.openfaas.gateway.here:8080/`

## [geoplanet-db/](geoplanet-db/)
This function looks up the Yahoo! [Where On Earth ID](https://en.wikipedia.org/wiki/WOEID) value for the geographic locations looked up in it.  Relies upon having a copy of the WOEID database in the container because Yahoo! killed this service some time ago, and as such only three copies seem to exist anywhere:

* https://archive.org/details/geoplanet_data_7.10.0.zip (needs to be loaded into a [SQLite](https://sqlite.org/) database)
* https://drwho.virtadpt.net/files/geoplanet_data_7.10.0.zip (needs to be loaded into a [SQLite](https://sqlite.org/) database)
* https://drwho.virtadpt.net/files/geoplanet.sqlite.zip (already loaded into a SQLite database, just uncompress)

### Building and deploying

### You already have a geoplanet.sqlite database:
* Make sure that the 'geoplanet.sqlite' file exists in your exocortex-faas/geoplabnet-db/ directory.  Put it there if it's not.
* `faas-cli build -f geoplanet-db.yml`
* `faas-cli deploy -f geoplanet-db.yml --gateway https://your.openfaas.gateway.here:8080/`

### You need to build a geoplanet.sqlite database:
```
user@host: sqlite3 geoplanet.sqlite
sqlite> .mode tabs
sqlite> PRAGMA foreign_keys=off;

sqlite> CREATE TABLE adjacencies (id INTEGER PRIMARY KEY, Place_WOE_ID TEXT, Place_ISO TEXT, Neighbour_WOE_ID TEXT, Neighbour_ISO TEXT);
sqlite> .import geoplanet_adjacencies_7.10.0.tsv temp_adjacencies
sqlite> INSERT INTO adjacencies(Place_WOE_ID, Place_ISO, Neighbour_WOE_ID, Neighbour_ISO) SELECT Place_WOE_ID, Place_ISO, Neighbour_WOE_ID, Neighbour_ISO from temp_adjacencies;
sqlite> drop table temp_adjacencies;

sqlite> CREATE TABLE admins (id INTEGER PRIMARY KEY, WOE_ID TEXT, iso TEXT, State TEXT, County TEXT, Local_Admin TEXT, Country TEXT, Continent TEXT);
sqlite> .import geoplanet_admins_7.10.0.tsv temp_admins
sqlite> INSERT INTO admins(WOE_ID, iso, State, County, Local_Admin, Country, Continent) SELECT WOE_ID, iso, State, County, Local_Admin, Country, Continent from temp_admins;
sqlite> drop table temp_admins;

sqlite> CREATE TABLE aliases (id INTEGER PRIMARY KEY, WOE_ID TEXT, Name TEXT, Name_Type TEXT, Language Text);
sqlite> .import geoplanet_aliases_7.10.0.tsv temp_aliases
sqlite> INSERT INTO aliases(WOE_ID, Name, Name_Type, Language) SELECT WOE_ID, Name, Name_Type, Language from temp_aliases;
sqlite> DROP TABLE temp_aliases;

sqlite> CREATE TABLE changes (id INTEGER PRIMARY KEY, Woe_id TEXT, Rep_id TEXT, Data_Version TEXT);
sqlite> .import geoplanet_changes_7.10.0.tsv temp_changes
sqlite> INSERT INTO changes (Woe_id, Rep_id, Data_Version) SELECT Woe_id, Rep_id, Data_Version from temp_changes;
sqlite> DROP TABLE temp_changes;

sqlite> CREATE TABLE places (id INTEGER PRIMARY KEY, WOE_ID TEXT, ISO TEXT, Name TEXT, Language TEXT, PlaceType TEXT, Parent_ID TEXT);
sqlite> .import geoplanet_places_7.10.0.tsv temp_places
sqlite> INSERT INTO places (WOE_ID, ISO, Name, Language, PlaceType, Parent_ID) SELECT WOE_ID, ISO, Name, Language, PlaceType, Parent_ID from temp_places;
sqlite> drop table temp_places;

sqlite> PRAGMA foreign_keys=on;
sqlite> VACUUM;
sqlite> .quit
```

Now follow the "You already have a geoplanet.sqlite database:" instructions above.

### How to use the Geoplanet database to look up WOEIDs:
`curl http://https://your.openfaas.gateway.here:8080/function/geoplanet-db/places/?Name=washington%20dc`

## [hmac-a-tron/](hmac-a-tron/)

### Building and deploying

## [httpbin/](httpbin/)

### Building and deploying

## [icanhazip/](icanhazip/)

### Building and deploying

## [testssl/](testssl/)

### Building and deploying

## [twitter-trends/](twitter-trends/)

### Building and deploying
