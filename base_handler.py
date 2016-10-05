#! usr/local/bin/env python3

import discord
import hidetoken # to hide token
import weather
import discord.ext.commands as c
import random

bot = c.Bot(command_prefix='>>',command_not_found="No command named {} found.",description='Weather & Forecast Bot',pm_help=True)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(enabled=True,
             help="request weather for a location indicator."
                  " location indicator can be as specific or vauge as you want. (invoke -forecast <location_indicator>)",
             pass_context = True)
async def forecast(ctx,*input_string:tuple):

    metric_units = False
    location = ''

    for i in input_string:
        word = ''.join(i)
        if word == '-save':
            await makeshortcut(ctx.message.author)
            continue
        if word == '-metric':
            metric_units = True
            continue
        location += "{} ".format(word)

    await bot.say(weather.get_forecast(location,metric_units))
    #print("location: {}".format(location))

async def makeshortcut(user : discord.Member):
    pass


bot.run(hidetoken.get_token())
