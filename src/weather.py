#!usr/local/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse as parse

HOST = 'https://query.yahooapis.com/v1/public/yql?q='
path = 'SELECT * from weather.forecast where (woeid) in ( SELECT woeid from geo.places(1) where text="{0}")' \
       ' and u="{1}"'

unit_system = {
    'imperial': {
        'distance': 'mi',
        'pressure': 'in',
        'speed': 'mph',
        'temp': 'F'
    },
    'metric': {
        'distance': 'km',
        'pressure': 'mb',
        'speed': 'km/h',
        'temp': 'C'
    }
}

emoji = [
    ':cloud_tornado:',
    ':thunder_cloud_rain: :worried:',
    ':thunder_cloud_rain:',
    ':thunder_cloud_rain:',
    ':thunder_cloud_rain:',
    ':sweat_drops: :snowflake:',
    ':cloud_rain:',
    ':cloud_snow:',
    ':snowflake: :cloud_rain:',
    ':cloud_rain:',
    ':snowflake: :cloud_rain:',
    ':cloud_rain:',
    ':cloud_rain:',
    ':cloud_snow:',
    ':cloud_snow:',
    ':dash: :cloud_snow:',
    ':cloud_snow: :snowman:',
    ':snowflake:',
    ':snowflake:',
    ':foggy:',
    ':foggy:',
    ':foggy',
    ':fog:',
    ':dash:',
    ':dash:',
    ':cold_sweat:',
    ':cloud:',
    ':cloud: :crescent_moon: :cloud:',
    ':white_sun_cloud:',
    ':cloud: :crescent_moon: :cloud:',
    ':white_sun_small_cloud:',
    ':full_moon:',
    ':sun_with_face: ',
    ':cloud: :full_moon:',
    ':white_sun_cloud:',
    ':cloud_rain:',
    ':sunny:',
    ':thunder_cloud_rain:',
    ':thunder_cloud_rain:',
    ':thunder_cloud_rain:',
    ':cloud_rain:',
    ':cloud_snow: :cloud_snow:',
    ':cloud_snow: :snowflake:',
    ':cloud_snow: :snowman: :snowflake:',
    ':white_sun_cloud:',
    ':thunder_cloud_rain:',
    ':cloud_snow:',
    ':thunder_cloud_rain:',
    ''
]


class WeatherException(Exception):
    def __init__(self, message):
        super(WeatherException, self).__init__(message)


def __verify(location: str):
    for word in location.split(' '):
        assert word.upper() not in ('SELECT', '*', 'ID', 'LOCATION', 'FROM', 'WHERE', 'UPDATE',
                                    'USER_ID', 'TIMES_REQUESTED', 'NAME', 'WOEID', 'WEATHER.FORECAST')


def __temp_emoji(temp, is_metric):
    COLD = 5 if is_metric else 40
    HOT = 25 if is_metric else 77
    if temp > HOT:
        return ':fire:'
    elif temp < COLD:
        return ':snowflake:'
    else:
        return ''


def __get(location, is_metric):
    full_path = parse.quote(path.format(location,'C' if is_metric else 'F'), safe='*()')
    query_string = HOST+full_path+'&format=json&callback='  # format
    req = requests.get(query_string) # throws requests.ConnectionError
    results = req.json()['query']['results'] # throws KeyError
    return results


def __format(location, yql_weather_results, unit_system):
    message_title = ''
    current_conditions = '**Current Conditions:** '
    forecast_today = '**Forecast for today**, '
    forecast_tomorrow = '**Forecast for tomorrow**, '
    forecast_threeday = '**Forecast for the day after tomorrow**, '

    if 'channel' in yql_weather_results:
        channel = yql_weather_results['channel']
        message_title += channel['title'] if 'title' in channel else 'Weather for "{}"'.format(location)
        if 'item' in channel:
            item = channel['item']

            if 'condition' in item:  # current condition & optional title date info
                condition = item['condition']
                message_title += ' ({})'.format(condition['date']) if 'date' in condition else '' # date not needed
                message_title += '\n'
                try:
                    try:
                        current_conditions += emoji[int(condition['code'])] if 'code' in condition else ''
                    except (ValueError, IndexError):
                        pass
                    current_conditions += ' '
                    current_conditions += '{0} at {1}{2}'.format(condition['text'], condition['temp'], unit_system['temp'])
                except KeyError:
                    current_conditions += 'Not Available.'

            else:
                current_conditions += 'Not Available.'
            current_conditions += '\n'
            if 'forecast' in item:
                try: # today's forecast
                    forecast = item['forecast'][0]
                    forecast_today += '{0} {1}:'.format(forecast['day'], forecast['date']) if 'day' and 'date' in forecast.keys() else ''
                    forecast_today += '\n'
                    forecast_today += '**Condition:**'
                    forecast_today += ' '
                    try:
                        forecast_today += emoji[int(forecast['code'])] if 'code' in forecast else ''
                    except (ValueError, IndexError):
                        pass
                    forecast_today += '{}'.format(forecast['text']) if 'text' in forecast else '*Not Available*'
                    forecast_today += ' '
                    forecast_today += 'high of '
                    forecast_today += '{0}{1}'.format(forecast['high'], unit_system['temp']) if 'high' in forecast.keys() else 'N/A'
                    try:
                        forecast_today += '{0}'.format(__temp_emoji(int(forecast['high']), unit_system['temp'] == 'C')) if 'high' in forecast.keys() else ''
                    except ValueError:
                        pass
                    forecast_today += ' & '
                    forecast_today += 'low of '
                    forecast_today += '{0}{1}'.format(forecast['low'], unit_system['temp']) if 'low' in forecast.keys() else 'N/A'
                    try:
                        forecast_today += '{0}'.format(__temp_emoji(int(forecast['low']), unit_system['temp'] == 'C')) if 'low' in forecast.keys() else ''
                    except ValueError:
                        pass
                except IndexError:
                    forecast_today += 'Not Available.'
                forecast_today += '\n'

                try: # tomorrow forecast
                    forecast = item['forecast'][1]
                    forecast_tomorrow += '{0} {1}:'.format(forecast['day'], forecast['date']) if 'day' and 'date' in forecast.keys() else ''
                    forecast_tomorrow += '\n'
                    forecast_tomorrow += '**Condition:**'
                    forecast_tomorrow += ' '
                    try:
                        forecast_tomorrow += emoji[int(forecast['code'])] if 'code' in forecast else ''
                    except (ValueError, IndexError):
                        pass
                    forecast_tomorrow += '{}'.format(forecast['text']) if 'text' in forecast else '*Not Available*'
                    forecast_tomorrow += ' '
                    forecast_tomorrow += 'high of'
                    forecast_tomorrow += ' '
                    forecast_tomorrow += '{0}{1}'.format(forecast['high'], unit_system['temp']) if 'high' in forecast.keys() else 'N/A'
                    try:
                        forecast_tomorrow += '{0}'.format(__temp_emoji(int(forecast['high']), unit_system['temp'] == 'C')) if 'high' in forecast.keys() else ''
                    except ValueError:
                        pass
                    forecast_tomorrow += ' & '
                    forecast_tomorrow += 'low of'
                    forecast_tomorrow += ' '
                    forecast_tomorrow += '{0}{1}'.format(forecast['low'], unit_system['temp']) if 'low' in forecast.keys() else 'N/A'
                    try:
                        forecast_tomorrow += '{0}'.format(__temp_emoji(int(forecast['low']), unit_system['temp'] == 'C')) if 'low' in forecast.keys() else ''
                    except ValueError:
                        pass
                except IndexError:
                    forecast_tomorrow += 'Not Available.'
                forecast_tomorrow += '\n'

                try: # three day forecast
                    forecast = item['forecast'][2]
                    forecast_threeday += '{0} {1}:'.format(forecast['day'], forecast['date']) if 'day' and 'date' in forecast.keys() else ''
                    forecast_threeday += '\n'
                    forecast_threeday += '**Condition:**'
                    forecast_threeday += ' '
                    try:
                        forecast_threeday += emoji[int(forecast['code'])] if 'code' in forecast else ''
                    except (ValueError, IndexError):
                        pass
                    forecast_threeday += '{}'.format(forecast['text']) if 'text' in forecast else '*Not Available*'
                    forecast_threeday += ' '
                    forecast_threeday += 'High of'
                    forecast_threeday += ' '
                    forecast_threeday += '{0}{1}'.format(forecast['high'], unit_system['temp']) if 'high' in forecast.keys() else 'N/A'
                    try:
                        forecast_threeday += '{0}'.format(__temp_emoji(int(forecast['high']), unit_system['temp'] == 'C')) if 'high' in forecast.keys() else ''
                    except ValueError:
                        pass
                    forecast_threeday += ' & '
                    forecast_threeday += 'low of'
                    forecast_threeday += ' '
                    forecast_threeday += '{0}{1}'.format(forecast['low'], unit_system['temp']) if 'low' in forecast.keys() else 'N/A'
                    try:
                        forecast_threeday += '{0}'.format(__temp_emoji(int(forecast['low']), unit_system['temp'] == 'C')) if 'low' in forecast.keys() else ''
                    except ValueError:
                        pass
                except IndexError:
                    forecast_threeday += 'Not Available.'
                forecast_threeday += '\n'

        if 'wind' in channel:
            wind = channel['wind']
            forecast_today += '**Wind Speed:**'
            forecast_today += ' '
            forecast_today += '{0} {1}'.format(wind['speed'],unit_system['speed']) if 'speed' in wind else 'N/A'
            forecast_today += ' '
            forecast_today += '**Wind Chill:**'
            forecast_today += ' '
            forecast_today += '{0} {1}'.format(wind['chill'],unit_system['temp']) if 'chill' in wind else 'N/A'
            forecast_today += '\n'
        if 'atmosphere' in channel:
            atmosphere = channel['atmosphere']
            forecast_today += '**Pressure:**'
            forecast_today += ' '
            forecast_today += '{0} {1}'.format(atmosphere['pressure'], unit_system['pressure']) if 'pressure' in atmosphere else 'N/A'
            forecast_today += ' '
            forecast_today += '**Visibility:**'
            forecast_today += ' '
            forecast_today += '{0} {1}'.format(atmosphere['visibility'], unit_system['distance']) if 'visibility' in atmosphere else 'N/A'
            forecast_today += '\n'
        if 'astronomy' in channel:
            astronomy = channel['astronomy']
            forecast_today += '**Sunrise:**'
            forecast_today += ' '
            forecast_today += '{0}'.format(astronomy['sunrise']) if 'sunrise' in astronomy else 'N/A'
            forecast_today += ' '
            forecast_today += '**Sunset:**'
            forecast_today += ' '
            forecast_today += '{0}'.format(astronomy['sunset']) if 'sunset' in astronomy else 'N/A'
            forecast_today += '\n'
    else:
        return '**No Weather Information Returned.**'

    return '{0}{1}{5}\n{2}{5}\n{3}{5}\n{4}\n'.format(message_title, current_conditions, forecast_today, forecast_tomorrow, forecast_threeday, ':heavy_minus_sign:')

def get_forecast(location, is_metric):
    try:
        location = __verify(location)
    except AssertionError:
        raise WeatherException('Bad Location Identifier')

    units = unit_system['metric'] if is_metric else unit_system['imperial']
    try:
        results = __get(location, is_metric)
    except (requests.ConnectionError, KeyError) as e:
        if isinstance(e, KeyError):
            raise WeatherException('No Weather Results Returned')
        else:
            raise WeatherException('Error Reaching Yahoo\'s Weather Database')
    if results is None:
        raise WeatherException('No Weather Results for location "{}"'.format(location))
    return __format(location, results, units)
