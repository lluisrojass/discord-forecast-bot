#! usr/local/bin/env python3

import requests
import urllib.parse as parse

yql_commands = {
    'woeid_path':'select woeid from geo.places(1) where text="{}"',
    'forecast_path':'select * from weather.forecast(1) where woeid="{}"',
    'host':'https://query.yahooapis.com/v1/public/yql?q=',
    'units':'u="C"',
    'format':"format=json",
    'delimeter':'&'
}


unit_system = {
    'imperial': {
        'distance':'mi',
        'pressure':'in',
        'speed':'mph',
        'temperature':'F'
    },
    'metric': {
        'distance':'km',
        'pressure':'mb',
        'speed':'km/h',
        'temperature':'C'
    }
}


def _get_woeid(place: str):
    """
     WOEID is Yahoo's own location identifier, due to YQL limitations
     forecast queries require either a WOEID or a location.
    :param place: identifier given to the bot to denote location
    :return: best guess WOEID based on place
    """

    url = yql_commands['woeid_path'].format(place)
    request_path = parse.quote(url,safe="*") + yql_commands['delimeter'] + yql_commands['format']
    query_string = yql_commands['host'] + request_path
    print(query_string)

    r = requests.request("GET",query_string) # throws requests.ConnectionError
    results = r.json()['query']['results']
    assert results != None

    return results['place']['woeid']  # potentially throwing  KeyError due to unpredictable result structure

def _get_weatherinfo(woeid: str,metric_units: bool):
    """
    :param woeid: id for finding weather
    :return: weather information dictionary
    """

    host = yql_commands['host']
    request_path = parse.quote(yql_commands['forecast_path'].format(woeid), safe="*")
    # special units
    request_path += (' and '+ parse.quote(yql_commands['units'])) if metric_units else ''
    request_path += yql_commands['delimeter'] + yql_commands['format']
    query_string = host + request_path
    print(query_string)
    r = requests.request("GET",query_string)
    results = r.json()['query']['results']

    # user input either too vague or very mispelled
    assert results != None

    return results

#TODO: use decorators for exception catching
def _format_data(weather_data: dict,units: dict):

    title = ''
    forecast_tomorow = 'Forecast for '
    forecast_today = 'Forecast for '
    line = '**--------------------------**'
    current_conditions = 'Current Conditions: '
    tomorrow_conditions = 'Forecast for '

    if 'channel' in weather_data:
        channel = weather_data['channel']
        title += '{0} '.format(channel['title'])
        if 'item' in channel:
            item = channel['item']
            # current condition & title information
            if 'condition' in item:
                condition = item['condition']
                title += '({0})'.format(condition['date'])
                current_conditions += "{0} at {1}{2}".format(condition['text'],condition['temp'],units['temperature'])
            # today and tomorrow's forecast
            if 'forecast' in item:
                forecast = item['forecast'][0]
                forecast_today += '{0} {1} (today):\n'.format(forecast['day'],forecast['date'])
                forecast_today += 'Condition: {}\n'.format(forecast['text'])
                forecast_today += 'High: {0} {2} Low: {1} {2}\n'.format(forecast['high'],forecast['low'],units['temperature'])

                forecast = item['forecast'][1]
                forecast_tomorow += '{0} {1} (tomorrow):\n'.format(forecast['day'],forecast['date'])
                tomorrow_conditions += 'Condition: {0}\n'.format(forecast['text'])
                tomorrow_conditions += 'High: {0} {2} Low: {1} {2}'.format(forecast['high'],forecast['low'],units['temperature'])
        if 'wind' in channel:
            wind = channel['wind']
            forecast_today += "Wind Speed: {0} {2}  Wind Chill: {1} {3}\n".format(wind['speed'],wind['chill'],units['speed'],units['temperature'])
        if 'atmosphere' in channel:
            atmosphere = channel['atmosphere']
            #TODO find out what rising is
            forecast_today += 'Pressure: {0} {4} Humidity: {1}% Visibility: {2} {3}\n'.format(atmosphere['pressure'],atmosphere['humidity'],atmosphere['visibility'],units['distance'],units['pressure'])
        if 'astronomy' in channel:
            astronomy = channel['astronomy']
            forecast_today += 'Sunrise: {0}  Sunset: {1}'.format(astronomy['sunrise'],astronomy['sunset'])

    line += '\n'
    title += '\n'
    forecast_today +='\n'
    current_conditions +='\n'
    tomorrow_conditions += '\n'

    return title + current_conditions + line + forecast_today  + line + forecast_tomorow + tomorrow_conditions





def get_forecast(location_text: str,metric_units=False):

    units =  unit_system['metric'] if metric_units is True else unit_system['imperial']

    try:
        woeid = _get_woeid(location_text)
    except (AssertionError):
        return "No weather information for this location"
    except (requests.ConnectionError, KeyError, TypeError) as err:
        return "issue resolving woeid, {}".format(err.args)

    try:
        raw_weather = _get_weatherinfo(woeid,metric_units)
    except  AssertionError:
        return "Location too vague, no weather results"
    except (requests.ConnectionError, TypeError) as err:
        return "Error when fetching weather info, {}".format(err.args)

    final_string = _format_data(raw_weather,units)

    return final_string








