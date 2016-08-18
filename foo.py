#! usr/local/bin/env python3

# fix the bloddy bad variable names
# implement asyncio lib
# refactor this mess

import json
import requests
import urllib.parse as parse
import urllib.error as error

# code value translates to position on array



yql_commands = {
    "constraints":"&limit 1&format=json",
    "woeid":"q=SELECT * from geo.places where text=",
    "forecast":"q=SELECT * from weather.forecast where woeid=",
    "host":"https://query.yahooapis.com/v1/public/yql?"
}

def get_weather(woeid):
    host = yql_commands['host']
    url = parse.quote((yql_commands["forecast"]+"{}"+yql_commands['constraints']).format(woeid),safe="&=*")
    query_string = host + url
    r = requests.request("GET",query_string)
    data = r.json()
    if not 'results' in data['query']:
        raise KeyError('query contains no results')
        return
    else:
        return data

def get_woeid(zip):
    url = parse.quote((yql_commands["woeid"]+"{}"+yql_commands["constraints"]).format(zip),safe="&=*")
    query_string = yql_commands['host'] + url
    try:
        r = requests.request("GET",query_string)
    except requests.ConnectionError as e:
        raise e

    data = r.json()
    try:
        woeid = data['query']['results']['place'][0]['woeid']
    except TypeError:
        print("zip code not resolved")
    print(woeid)
    return woeid

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


try:
    w = get_woeid("1454561")
except KeyError as k:
    print(k.__str__())

f = get_weather(w)
print(f)

