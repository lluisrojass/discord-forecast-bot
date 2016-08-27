#! usr/local/bin/env python3

# TODO: implement aiohttp lib
import requests
import urllib.parse as parse

yql_commands = {
    "format":"format=json",
    'woeid':'select * from geo.places where text="{}" LIMIT 1&',
    'forecast':'select * from weather.forecast where woeid="{}" LIMIT 1&',
    'host':'https://query.yahooapis.com/v1/public/yql?q='
}


def _get_woeid(place: str):
    """
     WOEID is Yahoo's own location identifier, due to YQL limitations
     forecast queries require either a WOEID or a location.
    :param place: identifier given to the bot to denote locaiton
    :return: best guess WOEID based on place
    """

    url = yql_commands["woeid"].format(place)
    url = parse.quote(url,safe="&*") + yql_commands["format"]
    query_string = yql_commands['host'] + url
    print(query_string)

    r = requests.request("GET",query_string) # throws requests.ConnectionError
    results = r.json()['query']['results'] # will not throw TypeError
    assert results != None

    woeid = results['place']['woeid'] # currently throwing unpredictable KeyError due to unconsistent result type
    print(woeid)
    return woeid


def _get_weatherinfo(woeid):
    host = yql_commands['host']
    url = parse.quote(yql_commands["forecast"].format(woeid),safe="&*")+yql_commands['format']
    query_string = host + url
    print(query_string)
    r = requests.request("GET",query_string)
    results = r.json()['query']['results']


    # user input either too vague or very mispelled
    assert results != None

    return results

    #TODO fix formatting of text

def _format_data(weather_data: dict):


    units_distance = ''
    units_pressure = ''
    units_temp = ''
    units_speed = ''
    forecast_status = ''
    forecast_date = ''
    forecast_day = ''
    forecast_tlow = ''
    forecast_thigh = ''
    forecast  = ''
    tom_status = ''
    tom_date = ''
    tom_day = ''
    tom_tlow = ''
    tom_thigh = ''
    wind = ''
    wind_chill = ''
    wind_speed = ''
    humidity  = ''
    pressure = ''
    atmosphere  = ''
    visibility  = ''
    astronomy = ''
    sunrise = ''
    sunset = ''


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
            # today and tomorrow's forecast
            if 'forecast' in item:
                forecast = item['forecast'][0]
                forecast_status = forecast['text'] if 'text' in forecast else 'N/A'
                forecast_date = forecast['date'] if 'date' in forecast else 'N/A'
                forecast_day = forecast['day'] if 'day' in forecast else 'N/A'
                forecast_tlow = forecast['low'] if 'low' in forecast else 'N/A'
                forecast_thigh = forecast['high'] if 'high' in forecast else 'N/A'
                forecast = item['forecast'][1]
            # tomorrow
                tom_status = forecast['text'] if 'text' in forecast else 'N/A'
                tom_date = forecast['date'] if 'date' in forecast else 'N/A'
                tom_day = forecast['day'] if 'day' in forecast else 'N/A'
                tom_tlow = forecast['low'] if 'low' in forecast else 'N/A'
                tom_thigh = forecast['high'] if 'high' in forecast else 'N/A'


    return ('{0} ({1})'.format(title,current_date)+ '\n'
    + 'Current Conditions: {0} at {1} {2}'.format(current_status,current_temp,units_temp) + '\n'
    + '**--------------------------**' + '\n'
    + 'Forecast for {0} {1} (today):'.format(forecast_day,forecast_date) + '\n'
    + 'Condition: {0}'.format(forecast_status) + '\n'
    + 'High: {0}{2}  Low: {1}{2}'.format(forecast_thigh,forecast_tlow,units_temp) + '\n'
    + 'Wind Speed: {0}{2}  Wind Chill: {1}{3}'.format(wind_speed,wind_chill,units_speed,units_temp) + '\n'
    + 'Sunrise: {0}  Sunset: {1} '.format(sunrise,sunset) + '\n'
    + 'Pressure: {0}{1} Humidity: {2}% Visibility: {3}{4}'.format(pressure,units_pressure,humidity,visibility,units_distance) + '\n'
    + '**--------------------------**' + '\n'
    + 'Forecast for {0} {1} (tomorrow)'.format(tom_day,tom_date) + '\n'
    + 'Condition: {0}'.format(tom_status) + '\n'
    + 'High: {0}{2} Low: {1}{2}'.format(tom_thigh,tom_tlow,units_temp) + '\n')

    #TODO: add personalized comment based on weather code thrown. :)

def get_forecast(location_text: str):

    try:
        w = _get_woeid(location_text)
    except (AssertionError):
        return "No Results for this location, maybe try more adding precision or check for misspellings"
    except (requests.ConnectionError, KeyError, TypeError) as err:
        return "issue resolving woeid, {}".format(err.args)

    try:
        raw_weather = _get_weatherinfo(w)
    except  AssertionError:
        return "Location too vague, no weather results"
    except (requests.ConnectionError, TypeError) as err:
        return "Error when fetching weather info, {}".format(err.args)

    finalstring = _format_data(raw_weather)

    return finalstring








