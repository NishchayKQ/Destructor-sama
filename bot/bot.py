# Note all dictionary keys are strings as json doesn't support integer keys
# using all intents rn u check if that's needed
# https://gist.github.com/lykn/bac99b06d45ff8eed34c2220d86b6bf4 button help
# m & s forum
"""
for dcData.json is single dict with list as value of keys
key will be server id, {serverid:[skullboard,delas-delete,vipChannel,💀,no of reactions,levelUpOn]

for starloglol.json
key will be server id, {serverid:[list of message ids]
"""

import time

# noinspection PyUnresolvedReferences
import delasDelete
# noinspection PyUnresolvedReferences
import skullboard
from level import on_message_increase_xp
from setup import *
from utility import amPamConverter

disconnectTime = None


@client.event
async def on_ready():
    print(f'destructor Sama has awoken {client.user}')
    for server in listOfServers:
        await tree.sync(guild=discord.Object(id=server))
    if channelID:
        channelToSend = client.get_channel(channelID)
        global disconnectTime

        current_time = time.localtime()
        if disconnectTime:
            ConnectTime = time.strftime("%H %M\n", current_time)
            timeLog = [disconnectTime + ConnectTime]
            await channelToSend.send(f"{amPamConverter(timeLog, mode=2)} ready for destruction!")
            disconnectTime = None
        else:
            ConnectTime = time.strftime("%H %M", current_time)
            await channelToSend.send(f"ready for destruction @{amPamConverter(ConnectTime)}")


@client.event
async def on_disconnect():
    global disconnectTime
    current_time = time.localtime()
    print(time.strftime("%H %M - from on_disconnect", current_time))
    if not disconnectTime:
        # current_time = time.localtime()
        disconnectTime = time.strftime("%H %M - ", current_time)


@client.event
async def on_resumed():
    global disconnectTime
    disconnectTime = None
    print("deleted a on resumed")


@client.event
async def on_guild_join(guild):
    with open("graphMods/dcData.json", mode="w") as ranaTigrina:
        ServerData.update({str(guild.id): [None, None, None, ["💀"], 3, None]})
        json.dump(ServerData, ranaTigrina, indent=4)
    with open("graphMods/starloglol.json", mode="w") as OceanMan:
        StarData.update({str(guild.id): []})
        json.dump(StarData, OceanMan, indent=4)
    updater(mode=2)


@client.event
async def on_guild_remove(guild):
    with open("graphMods/dcData.json", mode="w") as ranaTigrina:
        ServerData.pop(str(guild.id))
        json.dump(ServerData, ranaTigrina, indent=4)
    with open("graphMods/starloglol.json", mode="w") as OceanMan:
        StarData.pop(str(guild.id))
        json.dump(StarData, OceanMan, indent=4)
    updater(mode=2)


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Button", style=discord.ButtonStyle.primary)
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button, ):
        await interaction.response.edit_message(content="This is an edited button response!")


@tree.command(name="rockpapersizzler", description="what do u mean \"wtf is this command?\"",
              guilds=convertedGuilds)
async def rpc(interaction: discord.Interaction):
    badboisEmbed = discord.Embed(
        title=f"{interaction.user.display_name}'s game of rpc", description="insert something")

    # butaButton = discord.ui.Button(label = "1",style = discord.ButtonStyle.primary,custom_id = "one")
    # tfIsView = discord.ui.View().add_item(butaButton)
    await interaction.response.send_message(embed=badboisEmbed, view=Buttons())


@tree.command(name="say", description="Constructor-Sama Can speak!",
              guilds=convertedGuilds)
async def sayStuff(interaction: discord.Interaction, what_to_say: str, which_channel: discord.TextChannel = None):
    if interaction.user.id in owner:
        if not which_channel:
            which_channel = interaction.channel
        await which_channel.send(content=what_to_say)
        await interaction.response.send_message(content="oki dokie", ephemeral=True)
        await interaction.delete_original_response()
    else:
        await interaction.response.send_message(content="only KepKep can make me say stuff!", ephemeral=True)


@tree.context_menu(name="bookmark a message",
                   guilds=convertedGuilds)
async def bookmark(interaction: discord.Interaction, message: discord.Message):
    if message.content:
        await interaction.user.send(message.content)
    if message.attachments:
        for ara in message.attachments:
            await interaction.user.send(ara.url)
    if message.embeds:
        for ara in message.embeds:
            await interaction.user.send(embed=ara)
    await interaction.response.send_message('added to bookmark!', ephemeral=True)


@client.event
async def on_message(message: discord.Message):
    if message.interaction:
        await on_message_increase_xp(message, message.interaction.user)

    if message.author == client.user:
        return

    if message.content.startswith('venus'):
        await message.channel.send('Love is show! Misetekure~')

    if message.content.startswith('c sleep') and message.author.id in owner:
        await message.add_reaction("👍")
        await client.close()

    if message.content.startswith('cre') and message.author.id in owner:
        await message.add_reaction("👍")
        import os
        import sys
        os.execv(sys.executable, ['python'] + sys.argv)

    if message.guild and ServerData[str(message.guild.id)][5] and not message.author.bot:
        await on_message_increase_xp(message)


client.run(token, log_handler=handler)
