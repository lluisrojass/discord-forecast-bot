#! usr/local/bin/env python3

# TODO: implement aiohttp lib


import json
import requests
import urllib.parse as parse
import urllib.error as error
import time
# code value translates to position on array



yql_commands = {
    "constraints":"&limit 1&format=json",
    #TODO do not fetch * but fetch jst woeid
    "woeid":"q=SELECT * from geo.places where text=",
    "forecast":"q=SELECT * from weather.forecast where woeid=",
    "host":"https://query.yahooapis.com/v1/public/yql?"
}


def get_forecast(location_text: str):

    # throws assertion exception if results is None
    # throws requests.ConnectionError if connection failed
    # throws TypeError if 'woeid not'

    def get_woeid(zip: str):
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

        # user input either too vague or very mispelled
        assert results != None

        return results

    #TODO fix formatting of text

    def resolve_information(weather_data: dict):

        if 'channel' in weather_data:
            channel = weather_data['channel']
            title = channel['title']
            # unit information
            #TODO bake unit demands into query string instead of wasting time extracting
            if 'units' in channel:
                units = channel['units']
                units_distance = units['distance'] if 'distance' in units else ''
                units_pressure = units['pressure'] if 'pressure' in units else ''
                units_speed = units['speed'] if 'speed' in units else ''
                units_temp = units['temperature'] if 'temperature' in units else ''
            if 'wind' in channel:
                wind = channel['wind']
                wind_speed = wind['speed'] if 'speed' in wind else 'N/A'
                wind_chill = wind['chill'] if 'chill' in wind else 'N/A'
            if 'atmosphere' in channel:
                atmosphere = channel['atmosphere']
                humidity = atmosphere['humidity'] if 'humidity' in atmosphere else 'N/A'
                pressure = atmosphere['pressure'] if 'pressure' in atmosphere else 'N/A'
                #TODO find out what rising is
                visibility = atmosphere['visibility'] if 'visibility' in atmosphere else 'N/A'
            if 'astronomy' in channel:
                astronomy = channel['astronomy']
                sunrise = astronomy['sunrise'] if 'sunrise' in astronomy else 'N/A'
                sunset = astronomy['sunset'] if 'sunset' in astronomy else 'N/A'
            if 'item' in channel:
                item = channel['item']
                # current condition information
                if 'condition' in item:
                    condition = item['condition']
                    current_status = condition['text'] if 'text' in condition else 'N/A'
                    current_date = condition['date'] if 'date' in condition else 'N/A'
                    current_temp = condition['temp'] if 'temp' in condition else 'N/A'
                # today's forecast
                if 'forecast' in item:
                    forecast = item['forecast'][0]
                    forecast_status = forecast['text'] if 'text' in forecast else 'N/A'
                    forecast_date = forecast['date'] if 'date' in forecast else 'N/A'
                    forecast_day = forecast['day'] if 'day' in forecast else 'N/A'
                    forecast_tlow = forecast['low'] if 'low' in forecast else 'N/A'
                    forecast_thigh = forecast['high'] if 'high' in forecast else 'N/A'
                    forecast = item['forecast'][1]
                    tom_status = forecast['text'] if 'text' in forecast else 'N/A'
                    tom_date = forecast['date'] if 'date' in forecast else 'N/A'
                    tom_day = forecast['day'] if 'day' in forecast else 'N/A'
                    tom_tlow = forecast['low'] if 'low' in forecast else 'N/A'
                    tom_thigh = forecast['high'] if 'high' in forecast else 'N/A'


        print('{0} ({1})'.format(title,current_date))
        print('Current Conditions: {0} at {1} {2}'.format(current_status,current_temp,units_temp))
        print('--------------------------')
        print('Forecast for {0} {1} (today):'.format(forecast_day,forecast_date))
        print('Condition: {0}'.format(forecast_status))
        print('High: {0}{2}  Low: {1}{2}'.format(forecast_thigh,forecast_tlow,units_temp))
        print('Wind Speed: {0}{2}  Wind Chill: {1}{3}'.format(wind_speed,wind_chill,units_speed,units_temp))
        print('Sunrise: {0}  Sunset: {1} '.format(sunrise,sunset))
        print('Pressure: {0}{1} Humidity: {2}% Visibility: {3}{4}'.format(pressure,units_pressure,humidity,visibility,units_distance))



    a = time.time()
    try:
        w = get_woeid(location_text)
    except requests.ConnectionError as e:
        return "Error when connecting to YQL DB, {}".format(e)
    except AssertionError as e:
        return "No Results Found when fetching WOEID"
    except TypeError as e:
        return "TYPEERROR Found when fetching WOEID"

    try:
        raw_weather = get_weatherinfo(w)
    except requests.ConnectionError as e:
        return "Error when connecting to YQL DB, {}".format(e)
    except AssertionError as e:
        return "No Results Found when fetching weather information"
    except TypeError as e:
        return "TYPEERROR Found when fetching weather information"


    resolve_information(raw_weather)
    b = time.time()
    print('{}'.format(b-a))


    return raw_weather







w = get_forecast("bournemouth")
