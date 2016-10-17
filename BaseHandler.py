#! usr/local/bin/env python3
# -*- coding: utf-8 -*-

import Hidetoken  # to hide token from public github
import Weather
import discord.ext.commands as c
import asyncio
import PreferenceDatabase
import sys
from Errors import WeatherException
from Errors import DatabaseException

messages_to_delete = []

bot = c.Bot(command_prefix='>>', command_not_found="No command named {} found.",
            description='Weather & Forecast Bot', pm_help=True)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


async def cleanup():
    await bot.wait_until_ready()
    while not bot.is_closed:
        if len(messages_to_delete) is not 0:
            for msg in messages_to_delete:
                await bot.delete_message(msg)
            messages_to_delete.clear()
        await asyncio.sleep(60)  # task runs every 60 seconds


@bot.command(enabled=True, help="request weather for a location indicator."
             " Location indicator can be as specific or vague as you desired."
             " flags: -dm : receive weather information as personal message\n"
             "-metric: to receive weather information in metric units\n"
             "-save: to save location preference on a server specific DB."
                                "Can invoke >>me to receive user specific weather.\n",
             pass_context=True)
async def forecast(ctx, *input_string: tuple):
    bot.type()
    mssg = ''
    location = ''
    forecast.weather_message = ''
    # pre weather request vars
    forecast.channel = ctx.message.channel
    # weather request editing vars
    forecast.is_metric = False
    forecast.is_pming = False
    # post weather request vars
    forecast.is_saving = False
    forecast.is_flag_invalid = False

    def save():
        forecast.is_saving = True

    def metric():
        forecast.is_metric = True

    def private_message():
        forecast.is_pming = True

    def invalid_flag():
        forecast.is_flag_invalid = True

    flags = {
        "-save": save,
        "-metric": metric,
        "-dm": private_message
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

    try:
        forecast.weather_message += Weather.get_forecast(location, forecast.is_metric)
    except WeatherException:
        forecast.weather_message += '**Error Fetching Weather**: {0}'.format(sys.exc_info()[1])

    if forecast.is_pming:
        forecast.channel = ctx.message.author
        pm_msg = await bot.say("{} weather has been sent to your personal messages".format(ctx.message.author.mention))
        messages_to_delete.append(pm_msg)

    if forecast.is_saving:
        forecast.weather_message += make_shortcut(ctx, location, forecast.is_metric)

    if forecast.is_flag_invalid:
        forecast.weather_message += "\n:warning:**Flag(s) identified but not resolved." \
                                    " Invoke >>help to view all flags**"

    msg = await bot.send_message(forecast.channel, forecast.weather_message)
    messages_to_delete.append(msg)


@bot.command(enabled=True, pass_context=True)
async def me(ctx):
    weather_message = ":warning: **No Preference Saved for {}.**".format(ctx.message.author.mention)
    database = PreferenceDatabase.Database(ctx.message.server.id)
    try:
        location, is_metric = database.get_preference(ctx.message.author.id)
    except DatabaseException:
        pass
    else:
        weather_message = Weather.get_forecast(location, is_metric)
    del database

    await bot.whisper(weather_message)


def make_shortcut(ctx, location_string: str, is_metric):

    response = "Unknown Error saving preference."
    database = PreferenceDatabase.Database(ctx.message.server.id)

    try:
        outcome = database.create_preference(ctx.message.author.name, ctx.message.author.id, location_string, is_metric)
    except DatabaseException:
        response = "Error saving preference: {}".format(sys.exc_info()[1])
    else:
        if outcome:
            response = "Location preference stored, invoke >>me for personalized weather."
        else:
            response = "Location preference updated, invoke >>me for personalized weather."

    del database
    return "\n:warning:**{}.**".format(response)

bot.loop.create_task(cleanup())
bot.run(Hidetoken.get_token())
