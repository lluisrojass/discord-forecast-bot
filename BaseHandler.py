#! usr/local/bin/env python3
# -*- coding: utf-8 -*-

import hidetoken  # hide token
import Weather
import discord.ext.commands as c
import asyncio
import WeatherPreferenceDB


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
    location_string = ''
    forecast.weather_message = ''
    # pre weather request vars
    forecast.channel = ctx.message.channel
    # weather request editing vars
    forecast.is_metric = False
    forecast.is_pming = False
    # post weather request vars
    forecast.is_saving = False
    forecast.is_invalid_flag = False

    async def save():
        forecast.is_saving = True
    async def metric():
        forecast.is_metric = True
    async def private_message():
        forecast.is_pming = True
        forecast.channel = ctx.message.author

    def invalid_flag():
        forecast.is_invalid = True

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
                location_string += "{} ".format(word)

    forecast.weather_message += Weather.get_forecast(location_string, forecast.is_metric)

    if forecast.is_pming:
        pm_msg = await bot.say("{} weather has been sent to your personal messages".format(ctx.message.author.mention))
        messages_to_delete.append(pm_msg)

    if forecast.is_saving:
        forecast.weather_message += make_shortcut(ctx, location_string)

    if forecast.is_invalid_flag:
        forecast.weather += ":warning:**Flag(s) identified but not resolved." \
                            " Invoke >>help to view all flags**:warning:"

    msg = await bot.send_message(forecast.channel, forecast.weather_message)
    messages_to_delete.append(msg)


@bot.command(enabled=True, pass_context=True)
async def me(ctx, *flags):
    database = WeatherPreferenceDB.Database()
    database.connect(ctx.message.server.id)
    location = database.get_preference(ctx.message.author.id)
    Weather.get_forecast(location, False)

async def make_shortcut(ctx, location_string: str):
    return_string = "Unknown Error saving preference"
    database = WeatherPreferenceDB.Database()
    database.connect(ctx.message.server.id)
    outcome = database.create_preference(ctx.message.author.name, ctx.message.author.id, location_string)

    if outcome is 0:
        return_string = "Invalid location, preference not saved."
    elif outcome is 1:
        return_string = "Location preference updated, invoke >>me for personalized weather."
    elif outcome is 2:
        return_string = "Location preference stored, invoke >>me for personalized weather."
    elif outcome is 3:
        return_string = "Invalid connection to database, preference not saved."

    return ":warning:**{}**:warning:".format(return_string)

bot.loop.create_task(cleanup())
bot.run(hidetoken.get_token())
