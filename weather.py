#! usr/local/bin/env python3

# TODO: implement aiohttp lib
import requests
import urllib.parse as parse

yql_commands_toformat = {
    'woeid':'select woeid from geo.places(1) where text="{}"&',
    'forecast':'select * from weather.forecast(1) where woeid="{}"&',
    'host':'https://query.yahooapis.com/v1/public/yql?q=',
}

delimeter = "&"
i_units = "u=F"
m_units = "u=C"
format = "format=json"

units = {
    imperial = {
    'distance':'',
    'pressure':'',
    'speed':'',
    'temperature':''},
    imperial = {
    'distance':'',
    'pressure':'',
    'speed':'',
    'temperature':''}
}


def _get_woeid(place: str):
    """
     WOEID is Yahoo's own location identifier, due to YQL limitations
     forecast queries require either a WOEID or a location.
    :param place: identifier given to the bot to denote locaiton
    :return: best guess WOEID based on place
    """

    url = yql_commands_toformat["woeid"].format(place)
    url = parse.quote(url,safe="&*") + format
    print(url)
    query_string = yql_commands_toformat['host'] + url
    print(query_string)

    r = requests.request("GET",query_string) # throws requests.ConnectionError
    results = r.json()['query']['results'] # will not throw TypeError
    assert results != None

    woeid = results['place']['woeid'] # currently throwing unpredictable KeyError due to unconsistent result type
    return woeid

def _get_weatherinfo(woeid):
    """

    :param woeid:
    :return:
    """
    host = yql_commands_toformat['host']
    url = parse.quote(yql_commands_toformat["forecast"].format(woeid), safe="&*") + format
    query_string = host + url
    print(query_string)
    r = requests.request("GET",query_string)
    results = r.json()['query']['results']

    # user input either too vague or very mispelled
    assert results != None

    return results

    #TODO fix formatting of text

def _format_data(weather_data: dict):

    title = ''
    forecast_today = "Forecast for "
    line = '**--------------------------**\n'
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
                title += ')\n'
                current_conditions += "{0} at {1}{2}".format(condition['text'],condition['temp'],"UNITS")
            # today and tomorrow's forecast
            if 'forecast' in item:
                forecast = item['forecast'][0]
                forecast_today += forecast['day'] + ' ' + forecast['date'] + ' (today):' + '\n'
                forecast_today += 'Condition: ' + forecast['text'] +'\n'
                forecast_today += 'High: {0}{2} Low: {1}{2}\n'.format(forecast['high'],forecast['low'],"UNITS")
                forecast = item['forecast'][1]

                tomorrow_conditions += 'Forecast for {0} {1} (tomorrow):\n'.format(forecast['day'],forecast['date'])
                tomorrow_conditions += 'Condition: {0}\n'.format(forecast['text'])
                tomorrow_conditions += 'High: {0}{2} Low: {1}{2}'.format(forecast['high'],forecast['low'],"UNITS")
        if 'wind' in channel:
            wind = channel['wind']
            forecast_today += "Wind Speed: {0}{2}  Wind Chill: {1}{3}\n".format(wind['speed'],wind['chill'],"UNITS(SPEED)","UNITS(TEMP)")
        if 'atmosphere' in channel:
            atmosphere = channel['atmosphere']
            #TODO find out what rising is
            forecast_today += 'Pressure: {0}{4} Humidity: {1}% Visibility: {2}{3}\n'.format(atmosphere['pressure'],atmosphere['humidity'],atmosphere['visibility'],"UNITS(DISTANCE)","UNITS(PRESSURE)")
        if 'astronomy' in channel:
            astronomy = channel['astronomy']
            forecast_today += 'Sunrise: {0}  Sunset: {1}'.format(astronomy['sunrise'],astronomy['sunset'])

    forecast_today +='\n'
    current_conditions +='\n'
    tomorrow_conditions += '\n'

    return title + current_conditions + line + forecast_today  + line + tomorrow_conditions

    #TODO: add personalized comment based on weather code thrown. :)

def get_forecast(location_text: str):

    try:
        w = _get_woeid(location_text)
    except (AssertionError):
        return "No weather information for this location"
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








