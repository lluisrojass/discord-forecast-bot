#! usr/local/bin/env python3

import discord
import hidetoken  # hide token
import weather
import discord.ext.commands as c
import asyncio


messages_to_delete = []

bot = c.Bot(command_prefix='>>',command_not_found="No command named {} found.",description='Weather & Forecast Bot',pm_help=True)


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
    # weather request editing vars
    forecast.is_metric = False
    # post weather request vars

    async def save():
        await makeshortcut(ctx.message.author)
    async def metric():
        forecast.is_metric = True
    async def private_message():
        await bot.say("@{} weather has been sent to your personal messages".format(ctx.message.author), delete_after=3.5)
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

    forecast.weather_message += weather.get_forecast(location_string, forecast.is_metric)
    msg = await bot.send_message(forecast.channel, forecast.weather_message)
    messages_to_delete.append(msg)


async def makeshortcut(user : discord.Member):
    pass

bot.loop.create_task(cleanup())
bot.run(hidetoken.get_token())
