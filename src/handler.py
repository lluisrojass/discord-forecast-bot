#! usr/local/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
from discord.ext.commands import Bot

from hide_token import get_token  # to hide token from public github
from db import get_preference, add_preference, DatabaseException
from weather import get_forecast, WeatherException

logger = logging.getLogger('discord.handler')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='../logs/discord_info.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
debug_logger = logging.getLogger('discord')
debug_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../logs/discord_debug.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
debug_logger.addHandler(handler)

bot = Bot(command_prefix='>>', command_not_found="No command named {0} found.", description='Current Conditions & Forecast', pm_help=True)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(enabled=True, pass_context=True,)
async def forecast(ctx, *input_string: tuple):
    location = ''
    weather_msg = ''
    notifications = []
    forecast.channel = ctx.message.channel
    forecast.is_metric = False
    forecast.is_pm = False
    forecast.invalid_flag = False
    forecast.is_saving = False
    forecast.flagstring = ''

    def save():
        if not forecast.is_saving:
            forecast.flagstring += 's'
            forecast.is_saving = True

    def metric():
        if not forecast.is_metric:
            forecast.flagstring += 'm'
            forecast.is_metric = True

    def private_message():
        if not forecast.is_pm:
            forecast.flagstring += 'p'
            forecast.is_pm = True

    def invalid_flag():
        if not forecast.invalid_flag:
            forecast.flagstring += 'i'
            forecast.invalid_flag = True

    flags = {
        "-save": save,
        "-metric": metric,
        "-pm": private_message
    }

    for i in input_string:
        word = ''.join(i)
        try:
            flags[word]()
        except KeyError:
            if word[0] == "-":
                invalid_flag()
            else:
                location += "{} ".format(word)

    location = location.rstrip()

    is_from_server = not isinstance(ctx.message.server,type(None))
    logger_text = '{}'+' - User: {0} User ID: {1} Server Name: {2} ' \
                       'Server ID: {3} Location: {4} Flags: {5}'.format(ctx.message.author.name,
                                                                        ctx.message.author.id,
                                                                        ctx.message.server.name if is_from_server else 'N/A',
                                                                        ctx.message.server.id if is_from_server else 'N/A',
                                                                        location if location != '' else 'N/A',
                                                                        forecast.flagstring if not forecast.flagstring == '' else 'N/A')

    logger.info(logger_text.format('Forecast Request'))

    await bot.send_typing(forecast.channel)
    try:
        weather_msg += get_forecast(location, forecast.is_metric)
        logger.info(logger_text.format('Forecast Retrieved'))

        if forecast.is_pm:
            if is_from_server:
                forecast.channel = ctx.message.author
                await bot.say("Hey {}, weather information is being sent to your PMs.".format(ctx.message.author.mention))

        if forecast.is_saving: # only saves if no WeatherException caught, preventing useless saves
            notifications.append(':warning:**'+make_shortcut(ctx.message.author, ctx.message.server,  location, forecast.is_metric)+'**')

        if forecast.invalid_flag:
            notifications.append(":warning:**Flag(s) identified but not resolved. for all flags view github.com/lluisrojass/discord-weather-bot**")

        for m in notifications:
            weather_msg += m + '\n'

    except WeatherException:
        weather_msg += ':warning: {}'.format(sys.exc_info()[1])
        logger.info(logger_text.format('Error Retrieving Weather ({})'.format(sys.exc_info()[1])))

    await bot.send_message(forecast.channel, weather_msg)


@bot.command(enabled=True, pass_context=True)
async def me(ctx):
    is_from_server = not isinstance(ctx.message.server,type(None))
    logger_text = '{} -'+'User: {0} User ID: {1} Server Name: {2} Server ID: {3}'.format(ctx.message.author.name,
                                                                                         ctx.message.author.id,
                                                                                         ctx.message.server.name if is_from_server else 'N/A',
                                                                                         ctx.message.server.id if is_from_server else 'N/A'
                                                                                         )


    await bot.send_typing(ctx.message.channel)
    try:
        location, is_metric = get_preference(ctx.message.author.id)
        weather_msg = get_forecast(location, is_metric)
        logger.info(logger_text.format('Me Request') + ' Location: {0} Units: {1}'.format(location,
                                                                                          'Metric' if is_metric else 'Imperial'
                                                                                          ))
    except (DatabaseException, WeatherException):
        weather_msg = sys.exc_info()[1]
        logger.info(logger_text.format('Me Request Failed ({})'.format(weather_msg)))

    if (not isinstance(ctx.message.server,type(None))):
        await bot.say("Hey {}, weather information is being sent to your PMs.".format(ctx.message.author.mention))
    await bot.whisper(weather_msg)


def make_shortcut(user, server, location, is_metric):
    is_from_server = not isinstance(server,type(None))
    logger_text = '{} - '+'User: {0} User ID: {1} Server Name: {2} Server ID: {3} Desired Location Update: {4}'.format(user.name,
                                                                                                       user.id,
                                                                                                       server.name if is_from_server else 'N/A',
                                                                                                       server.id if is_from_server else 'N/A',
                                                                                                       location)
    try:
        did_create = add_preference(location, is_metric, user.name, user.id)
        response = 'Weather preference created' if did_create else 'Weather preference updated'
        logger.info(logger_text.format(response))
    except DatabaseException:
        response = sys.exc_info()[1]
        logger.info(logger_text.format('Preference update failed injection validation'))

    return response


bot.run(get_token())
