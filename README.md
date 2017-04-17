# Discord Weather Bot (4CAST)

## Invite
Invite 4CAST Weather Bot to your server [here](https://discordapp.com/oauth2/authorize?client_id=220798987777605632&scope=bot&permissions=52224)
## Description
4CAST is a Discord Bot to fetch & provide weather conditions and 3 day forecast. Weather data is provided by Yahoo's [YQL](https://developer.yahoo.com/yql/) weather endpoint. Application implements the [Discord.py](https://github.com/Rapptz/discord.py) API to speak to your guild.
## Commands

```LiveScript
>>forecast <location> [-metric] [-pm] [-save]
```
Create a weather request based on `<location>`.

#### Flags
flags must be space seperated


`-metric` Request weather in metric units.

`-pm` Receive results as a private messsage.

`-save` Save this request for expedited requesting with a `>>me` command.

```LiveScript
>>me
```
Invoke to receive personalized weather based on saved location (server independent).

# Example
![prototype](https://i.gyazo.com/75d89cd86e57a8602c6fccde67386c8f.gif)
