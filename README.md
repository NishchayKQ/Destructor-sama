# setup
## To host it yourself, follow these steps :
1. add IDs of owners on line no 30 of bot.py in a List [ID1,ID2...]
    Example: 
        Multiple Owners
            `owner = [534258961044444444, 867496941999999999]`
        Single Owner
            `owner = [534258961044444444]`
`
    Note: Owners can restart or switch the bot off / make the bot say stuff
          in particular channel...No other permissions are given like the ability
          to change skullBoard...

2. add IDs of server you want the slash commands to work on in a list  [ID1,ID2...]
    (line no. 31)

3. (optional , line no 32) mention ID of a channel you want the bot to send messages like
        *bot is now online*
4. Finally on line no 33 , add your token...[here](https://discordpy.readthedocs.io/en/stable/discord.html) is more info on how to get your token 


# My discord bot with features:
## Multiple emoji starboard
the bot will post a message in x channel when y amount of reactions are detected
on a message. Note x and y can be customized as well

## Leveling feature
creates a rank card generated with my handwriting by image manipulation

## bookmark a message on a server
context menu for a message gives option to send that message to your dm

## log deleted messages
can log deleted messages and post them to a channel of choice

# Some important info:
## *c sleep*
Owners of the bot can run this to make the bot offline

## *cre*
restarts the bot with any modifications on bot.py if any
