import json
import logging

import discord

# List of owner IDs
owner: list[discord.User.id] = []

# id of servers you want the bot to work in
listOfServers: list[discord.Guild.id] = []

# Channel ID the bot will post if it's online!
channelID: discord.TextChannel.id = 0

# add your token
token: str = ""

# don't add anything from here onwards

handler = logging.FileHandler(filename='graphMods/discord.log', encoding='utf-8', mode='w')

with open("graphMods/dcData.json") as araFile:
    ServerData = json.load(araFile)
with open("graphMods/starloglol.json") as nyaFile:
    StarData = json.load(nyaFile)
with open("graphMods/level.json") as frenchFile:
    LevelData = json.load(frenchFile)

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

convertedGuilds = []
for server in listOfServers:
    convertedGuilds.append(discord.Object(id=server))


def updater(mode: int = 1, update_level: dict = None):
    global ServerData, StarData, LevelData
    if mode == 1:  # default mode which is to update ServerData
        with open("graphMods/dcData.json") as erisFile:
            ServerData = json.load(erisFile)
    elif update_level:
        with open("graphMods/level.json", mode="w") as ireFile:
            json.dump(update_level, ireFile, indent=4)
        # with open("graphMods/level.json") as araFile:
        #   levelData = json.load(araFile)
        LevelData = update_level
        # print(f" from upDater {levelData}")
    else:  # update all usually I use mode 2 for this
        with open("graphMods/dcData.json") as erisFile:
            ServerData = json.load(erisFile)
        with open("graphMods/starloglol.json") as mewFile:
            StarData = json.load(mewFile)
        with open("graphMods/level.json") as ireFile:
            LevelData = json.load(ireFile)
