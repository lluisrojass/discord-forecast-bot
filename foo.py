#! usr/local/bin/env python3

import urllib.parse as url_parse
import urllib.request as url_request
import json
import urllib.error as e

yql_delimiter="limit 1"
yql_AND="&"
yql_json_format = "format=json"
yql_host = 'https://query.yahooapis.com/v1/public/yql?q='
yql_pullwoeid = "SELECT * from geo.places where text="
yql_pullforecast = "SELECT * from weather.forecast where location="



def get_woeid(zip):
    yql_querystring = url_parse.quote(yql_pullwoeid + zip + yql_AND + yql_json_format + yql_AND + yql_delimiter,safe="&*=")
    yql_uri = yql_host + yql_querystring
    print(yql_uri)
    try:
        geoinfo_json = url_request.urlopen(yql_uri).read().decode('utf-8')
    except e.HTTPError:
        print("cannot resolve socket")
        return

    json_string = json.loads(geoinfo_json)



    print(type(json_string))
    #print(json_string['query']['results']['place'][0]['admin2']['woeid'])






get_woeid("")