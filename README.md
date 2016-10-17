# Discord Weather Bot

Invite this Bot to your server with [this link](https://discordapp.com/oauth2/authorize?client_id=220798987777605632&scope=bot&permissions=52224)!

Discord Bot to fetch & provide weather conditions and 3 day forecast when provided with location information. Weather information provided by Yahoo! using [YQL database](https://developer.yahoo.com/yql/). written in Python 3.5, implements the [Discord.py](https://github.com/Rapptz/discord.py) API. 

Available Commands:

*>>forecast* \<location-indicator> [optional flags]: Location indicator can be as vague as desired, and can range from zip codes to full addresses to National Parks (if too vague, user will be notified). Optional flags: **[-metric]**: To receive weather information in metric units instead of default imperial units. **[-pm]**: for receiving info in personal messages instead of the public chat. **\[-save]**: To save or update location on server specific SQL table, after preference is saved weather information can be expedited with a *>>me* command. Desired unit preference also saved if -metric flag present.

*>>me*: Invoke to receive personalized weather based on saved location in server specific SQL table. 

*>>help*: Invoke to receive help message with all commands and flags to personal messages. 
