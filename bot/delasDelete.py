from setup import *


@tree.command(name="setup_delas-delete",
              description="channel where deleted messages go | passing no arguments will disable this feature",
              guilds=convertedGuilds)
@discord.app_commands.checks.has_permissions(administrator=True)
async def delSet(interaction: discord.Interaction, which_channel: discord.TextChannel = None):
    particularServerData = ServerData[str(interaction.guild_id)]
    if which_channel:
        particularServerData[1] = which_channel.id
    else:
        particularServerData[1] = None
    ServerData.update({str(interaction.guild_id): particularServerData})
    with open("graphMods/dcData.json", mode="w") as araFile:
        json.dump(ServerData, araFile, indent=4)
    updater()
    await interaction.response.send_message(content="okie dokie")


@delSet.error
async def delSet_error(interaction, error):
    if error == "You are missing Administrator permission(s) to run this command.":
        await interaction.response.send_message(content=error)
    else:
        raise error


@client.event
async def on_raw_message_delete(message):
    channelToSendID = None
    if message.guild_id:  # haha if message is ephemeral or dm message delete then ignore
        channelToSendID = ServerData[str(message.guild_id)][1]
    if channelToSendID:
        try:
            if message.channel_id == channelToSendID:
                raise AttributeError("not this channel lmao")
            if message.cached_message.author.id in owner:
                print("kepkep message eh")
            kawaiestEmbed = discord.Embed(
                description=message.cached_message.content, timestamp=message.cached_message.created_at)
            try:
                kawaiestEmbed.set_author(
                    name=message.cached_message.author.display_name, icon_url=message.cached_message.author.avatar.url)
            except AttributeError:
                kawaiestEmbed.set_author(
                    name=message.cached_message.author.display_name)

            kawaiestEmbed.set_footer(text=message.cached_message.channel.name)

            channelToSend = client.get_channel(channelToSendID)
            if not channelToSend:
                particularServerData = ServerData[str(message.guild_id)]
                particularServerData[1] = None
                ServerData.update(
                    {str(message.guild_id): particularServerData})
                with open("graphMods/dcData.json", mode="w") as araFile:
                    json.dump(ServerData, araFile, indent=4)
                updater()
                raise AttributeError("channel deleted")
            await channelToSend.send(embed=kawaiestEmbed)
        except AttributeError:
            pass
