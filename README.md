# Discord Weather Bot (4CAST)

Invite 4CAST Bot to your server [here!](https://discordapp.com/oauth2/authorize?client_id=220798987777605632&scope=bot&permissions=52224)!

4CAST is a Discord Bot to fetch & provide weather conditions and 3 day forecast when provided with location information. Weather information provided by Yahoo! using [YQL](https://developer.yahoo.com/yql/). written in Python 3 and implements the [Discord.py](https://github.com/Rapptz/discord.py) API. 

Available Commands:

`>>forecast location-indicator [<-metric>] [<-pm>] [<-save>]`

Location indicator can be as vague as desired and accepted identifiers range from full addresses to national parks. 

**Optional flags**: 

*-metric*: Receive weather information in metric units instead of imperial units (default). 

*-pm*: Receive weather in personal messages instead of public server chat. 

*-save*: Save or update location on server specific db. After preference is saved weather information can be expedited with a >>me command. Desired unit preference also saved if present.

`>>me` Invoke to receive personalized weather based on saved location (server specific). 

`>>help` Invoke to receive help message with all commands and optional flags. Sent to personal messages. 
