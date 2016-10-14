#! usr/local/bin/env python3

import discord
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


@bot.command(enabled=True,help="request weather for a location indicator."
             " location indicator can be as specific or vague as you want."
             " (invoke >>forecast <location_indicator>)",
             pass_context=True)
async def forecast(ctx, *input_string: tuple):
    location_string = ''
    forecast.weather_message = ''
    # pre weather request vars
    forecast.channel = ctx.message.channel
    forecast.is_pming = False
    # weather request editing vars
    forecast.is_metric = False
    # post weather request vars
    forecast.is_saving = False

    async def save():
        forecast.is_saving = True
    async def metric():
        forecast.is_metric = True
    async def private_message():
        forecast.is_pming = True
        forecast.channel = ctx.message.author

    def invalid_flag():
        forecast.weather_message += ":warning:A flag was identified but not resolved." \
                                    " invoke >>help to view all flags:warning:\n\n"

    flags = {
        "-save": save,
        "-metric": metric,
        "-dm": private_message
    }

    for i in input_string:
        word = ''.join(i)
        try:
            await flags[word]()
        except KeyError:
            if word[0] == "-":
                invalid_flag()
            else:
                location_string += "{} ".format(word)

    if forecast.is_saving:
        await make_shortcut(ctx, location_string)
    if forecast.is_pming:
        await bot.say("@{} weather has been sent to your personal messages".format(ctx.message.author))
    forecast.weather_message += Weather.get_forecast(location_string, forecast.is_metric)
    msg = await bot.send_message(forecast.channel, forecast.weather_message)
    messages_to_delete.append(msg)


async def make_shortcut(ctx, location_string: str):
    database = WeatherPreferenceDB.Database()
    print(location_string)
    print(ctx.message.author.id)
    if database.create_preference(ctx, location_string):
        await bot.say('preference has been saved')  # TODO: mention user
    else:
        await bot.say('preference has been updated')  # TODO: mention user

bot.loop.create_task(cleanup())
bot.run(hidetoken.get_token())
