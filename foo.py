#! usr/local/bin/env python3

# TODO: implement aiohttp lib


import json
import requests
import urllib.parse as parse
import urllib.error as error

# code value translates to position on array



yql_commands = {
    "constraints":"&limit 1&format=json",
    #TODO do not fetch * but fetch jst woeid
    "woeid":"q=SELECT * from geo.places where text=",
    "forecast":"q=SELECT * from weather.forecast where woeid=",
    "host":"https://query.yahooapis.com/v1/public/yql?"
}


def get_forecast(location_text):

    # throws assertion exception if results is None
    # throws requests.ConnectionError if connection failed
    # throws TypeError if 'woeid not'
    # admin2: information on County, Province, Parish, Department, District
    # admin3: information on Commune, Municipality, District, Ward.

    def get_woeid(zip):
        url = parse.quote((yql_commands["woeid"]+"'{}'"+yql_commands["constraints"]).format(zip),safe="&=*")
        query_string = yql_commands['host'] + url

        #will throw requests.ConnectionError if failed connection
        r = requests.request("GET",query_string)

        # will NOT throw TypeError
        results = r.json()['query']['results']
        assert results != None

        # will NOT throw TypeError if assertion passed
        woeid = results['place'][0]['woeid']
        return woeid


    def get_weatherinfo(woeid):
        host = yql_commands['host']
        url = parse.quote((yql_commands["forecast"]+"{}"+yql_commands['constraints']).format(woeid),safe="&=*")
        query_string = host + url

        r = requests.request("GET",query_string)
        results = r.json()['query']['results']

        # user input either too vague or extremely mispelled
        assert results != None

        return results



    try:
        w = get_woeid(location_text)
    except requests.ConnectionError as e:
        return "Error when connecting to YQL DB, {}".format(e)
    except AssertionError as e:
        return "No Results Found when fetching WOEID"
    except TypeError as e:
        return "TYPEERROR Found when fetching WOEID"

    print("WOEID FOR WELLINGTON: " +  w)

    try:
        raw_weather = get_weatherinfo(w)
    except requests.ConnectionError as e:
        return "Error when connecting to YQL DB, {}".format(e)
    except AssertionError as e:
        return "No Results Found when fetching weather information"
    except TypeError as e:
        return "TYPEERROR Found when fetching weather information"


    return raw_weather












#TODO fix formatting of text

# def resolve_information(weather_data: dict):
#     u_distance,u_speed,u_temp,u_pressure = ""
#     current_status,current_date = ""
#     title = ""
#     title = weather_data['title'] if 'title' in weather_data else ""
#
#     curr_object = None
#     if 'channel' in weather_data:
#         curr_object = weather_data['channel']
#         u_distance = curr_object['distance'] if 'distance' in channel else ''
#         u_pressure = channel['pressure'] if 'pressure' in channel else ''
#         U_speed = channel['speed'] if 'speed' in channel else ''
#         u_temp = channel['temperature'] if 'temperature' in channel else ''
#
#
#
#     # current weather condition
#     if 'condition' in weather_data:
#         condition = weather_data['condition']
#         code = condition['code'] if 'code' in condition else ''
#         current_status = condition['text'] if 'text' in condition AND else 'N/A'
#         current_date = condition['date'] if 'date' in condition else 'N/A'
#     if 'forecast' in


w = get_forecast("Wellington")
print(w)
