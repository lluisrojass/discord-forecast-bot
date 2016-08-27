#! usr/local/bin/env python3

import discord
import _token # to hide token
import weather
import discord.ext.commands as c

#bot = c.Bot(command_prefix='?',description='Bot to provide weather information based on provided location')
client = discord.Client()
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#TODO convert to event
@client.event
async def on_message(message):
    # check if messsage is from bot
    if (message.author == client.user):
        return

    if (message.content.startswith("!forecast")):
        location = (message.content.lstrip("!forecast")).strip()
        await client.send_message(message.channel,weather.get_forecast(location))


client.run(_token.get_token())
