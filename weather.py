#! usr/local/bin/env python3

import requests
import urllib.parse as parse

yql_commands = {
    'host': 'https://query.yahooapis.com/v1/public/yql?q=',
    'woeid_path': 'select woeid from geo.places(1) where text="{}"',
    'forecast_path': 'select * from weather.forecast(1) where woeid="{}"',
    'url_delimiter': '&',
    'yql_delimiter': ' and ',
    'metric_units': 'u="C"',
    'format': "format=json"
}

unit_system = {
    'imperial': {
        'distance': 'mi',
        'pressure': 'in',
        'speed': 'mph',
        'temperature': 'F'
    },
    'metric': {
        'distance': 'km',
        'pressure': 'mb',
        'speed': 'km/h',
        'temperature': 'C'
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
    request_path = parse.quote(url, safe="*") + yql_commands['url_delimiter'] + yql_commands['format']
    query_string = yql_commands['host'] + request_path
    print(query_string)

    r = requests.get(query_string)  # throws requests.ConnectionError
    results = r.json()['query']['results']

    assert results is not None

    return results['place']['woeid']  # potentially throwing  KeyError due to unpredictable result structure

def _get_weatherinfo(woeid: str,metric_units: bool):

    """
    :param woeid: id for finding weather
    :return: weather information dictionary
    """

    host = yql_commands['host']
    request_path = parse.quote(yql_commands['forecast_path'].format(woeid), safe="*")
    # unit preference
    request_path += (parse.quote(yql_commands['yql_delimiter'] + yql_commands['metric_units'])) if metric_units else ''
    # require JSON results
    request_path += yql_commands['url_delimiter'] + yql_commands['format']

    query_string = host + request_path
    print(query_string)
    r = requests.get(query_string)
    results = r.json()['query']['results']

    # user input either too vague or very misspelled
    assert results is not None
    return results

# TODO: use decorators for exception catching


def _format_data(weather_data: dict, units: dict):

    message_title = ''
    current_conditions = 'Current Conditions: '
    forecast_today = 'Forecast for '
    forecast_tomorrow = 'Forecast for '
    forecast_threeday = 'Forecast for '
    line = '**--------------------------**\n'

    if 'channel' in weather_data:
        channel = weather_data['channel']
        message_title += channel['title']
        if 'item' in channel:
            item = channel['item']
            # current condition & title information
            if 'condition' in item:
                condition = item['condition']
                message_title += ' ({})\n'.format(condition['date'])
                current_conditions += "{0} at {1}{2}\n".format(condition['text'],
                                                               condition['temp'], units['temperature'])
            # three day forecast information
            if 'forecast' in item:
                # today's forecast
                try:
                    forecast = item['forecast'][0]
                    forecast_today += '{0} {1}:\n'.format(forecast['day'], forecast['date'])
                    forecast_today += 'Condition: {}\n'.format(forecast['text'])
                    forecast_today += 'High: {0} {2} Low: {1} {2}\n'.format(forecast['high'],
                                                                            forecast['low'], units['temperature'])
                except IndexError:
                    forecast_today += 'Not Available.\n'
                # tomorrow forecast
                try:
                    forecast = item['forecast'][1]
                    forecast_tomorrow += '{0} {1}:\n'.format(forecast['day'], forecast['date'])
                    forecast_tomorrow += 'Condition: {0}\n'.format(forecast['text'])
                    forecast_tomorrow += 'High: {0} {2} Low: {1} {2}\n'.format(forecast['high'],
                                                                               forecast['low'], units['temperature'])
                except IndexError:
                    forecast_tomorrow += 'Not Available.\n'
                # three day forecast
                try:
                    forecast = item['forecast'][2]
                    forecast_threeday += '{0} {1}:\n'.format(forecast['day'],forecast['date'])
                    forecast_threeday += 'Condition: {0}\n'.format(forecast['text'])
                    forecast_threeday += 'High: {0} {2} Low: {1} {2}\n'.format(forecast['high'],
                                                                               forecast['low'], units['temperature'])
                except IndexError:
                    forecast_threeday += 'Not Available.\n'

        if 'wind' in channel:
            wind = channel['wind']
            forecast_today += "Wind Speed: {0} {2}" \
                              " Wind Chill: {1} {3}\n".format(wind['speed'], wind['chill'], units['speed'],
                                                              units['temperature'])
        if 'atmosphere' in channel:
            atmosphere = channel['atmosphere']
            # TODO find out what rising is
            forecast_today += 'Pressure: {0} {4} Humidity: {1}% ' \
                              'Visibility: {2} {3}\n'.format(atmosphere['pressure'], atmosphere['humidity'],
                                                             atmosphere['visibility'], units['distance'],
                                                             units['pressure'])
        if 'astronomy' in channel:
            astronomy = channel['astronomy']
            forecast_today += 'Sunrise: {0}  Sunset: {1}\n'.format(astronomy['sunrise'], astronomy['sunset'])

    return "{0}{1}{2}{3}{2}{4}{2}{5}".format(message_title, current_conditions,
                                             line, forecast_today, forecast_tomorrow, forecast_threeday)


def get_forecast(location_text: str, metric_units=False):
    units = unit_system['metric'] if metric_units is True else unit_system['imperial']

    try:
        woeid = _get_woeid(location_text)
    except AssertionError:
        return "No weather information available for the provided location, location may be too vague."
    except (KeyError, TypeError):
        return "Error encountered resolving WOEID."
    except requests.ConnectionError:
        return "Unable to reach Yahoo! Weather."

    try:
        raw_weather = _get_weatherinfo(woeid, metric_units)
    except AssertionError:
        return "No weather information received, location may be too vague. "
    except TypeError:
        return "Error fetching weather information"
    except requests.ConnectionError:
        return "Unable to reach Yahoo! Weather."

    try:
        final_string = _format_data(raw_weather, units)
    except KeyError:
        return "Error resolving weather data."

    return final_string








