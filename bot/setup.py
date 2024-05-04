import json
import logging
import sqlite3
from enum import Enum

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

con = sqlite3.connect("graphMods/servers.db")
cur = con.cursor()

with open("graphMods/starloglol.json") as nyaFile:
    StarData = json.load(nyaFile)
with open("graphMods/level.json") as frenchFile:
    LevelData = json.load(frenchFile)


class Config(Enum):
    skull: callable = "skull_ch"
    delas: callable = "delas_ch"
    level: callable = "level_ch"
    multi: callable = "level_multi"
    rxn: callable = "no_of_rxn"
    emojis: callable = "emojis"

    def __call__(self, server_id: int) -> int | list | None:
        res = con.execute(f"select {self.value} from config where id = {server_id}").fetchone()[0]
        if res is not None:
            if self is Config.emojis:
                return eval(res)
            else:
                return res

    def __setitem__(self, key, value):
        if value is list:
            con.execute(f"update config set {self.value} = {repr(value)} where id = {key}")
        else:
            con.execute(f"update config set {self.value} = ? where id = {key}", (value,))
        con.commit()


intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

convertedGuilds = []
for server in listOfServers:
    convertedGuilds.append(discord.Object(id=server))


def updater(mode: int = 1, update_level: dict = None):
    global StarData, LevelData
    if update_level:
        with open("graphMods/level.json", mode="w") as ireFile:
            json.dump(update_level, ireFile, indent=4)
        # with open("graphMods/level.json") as araFile:
        #   levelData = json.load(araFile)
        LevelData = update_level
        # print(f" from upDater {levelData}")
    else:  # update all usually I use mode 2 for this
        with open("graphMods/starloglol.json") as mewFile:
            StarData = json.load(mewFile)
        with open("graphMods/level.json") as ireFile:
            LevelData = json.load(ireFile)
