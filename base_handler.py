#! usr/local/bin/env python3

import discord
import _token # to hide token
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



@client.event
async def on_message(message):
    # check if messsage is from bot
    if (message.author == client.user):
        return
    if (message.content.startswith("!forecast")):
        zipcode = message.content.strip("!forecast ")
        await client.send_message(message.channel,zipcode)



client.run(_token.get_token())
