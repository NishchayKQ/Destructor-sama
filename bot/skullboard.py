from setup import *


@tree.command(name="setup_skullboard",
              description="manage or add skullboard | passing no arguments will disable this feature",
              guilds=convertedGuilds)
@discord.app_commands.checks.has_permissions(administrator=True)
@discord.app_commands.describe(emojis="can enter multiple, only recognises gold variant for coloured emojis like 👍👍🏽")
@discord.app_commands.describe(channel="channel where destructor will post in")
@discord.app_commands.describe(
    number_of_reactions="no. of reactions for a message to get posted in skullboard...default is 3")
async def skullSet(interaction: discord.Interaction, channel: discord.TextChannel = None, emojis: str = None,
                   number_of_reactions: int = None):
    try:
        particularServerData = ServerData[str(interaction.guild_id)]
        if channel:
            particularServerData[0] = channel.id
        await interaction.response.send_message(content="okie dokie")
        if emojis:
            cont = False
            toPrint = ""
            emojis = "".join(emojis.split())
            listOfEmojis = []
            for ara in emojis:
                if ara == "<":
                    cont = True
                if ara == ">":
                    cont = False
                    toPrint = toPrint + ara
                    listOfEmojis.append(toPrint)
                    toPrint = ""
                    continue
                if cont:
                    toPrint = toPrint + ara
                    continue
                if ord(ara) in [127995, 127996, 127997, 127998, 127999, 65039]:
                    continue  # remove colour variation selectors
                listOfEmojis.append(ara)

            listOfEmojis = list(set(listOfEmojis))
            print("------------------------")
            print(listOfEmojis)
            print("------------------------")
            particularServerData[3] = listOfEmojis
            message = await interaction.original_response()
            for ara in listOfEmojis:
                await message.add_reaction(ara)

        if number_of_reactions:
            particularServerData[4] = number_of_reactions

        if not channel and not emojis and not number_of_reactions:
            particularServerData[0] = None

        ServerData.update({str(interaction.guild_id): particularServerData})
        with open("graphMods/dcData.json", mode="w") as araFile:
            json.dump(ServerData, araFile, indent=4)
        updater()
    except discord.errors.HTTPException:
        await interaction.channel.send(content="emoji not found")


@skullSet.error
async def skullSet_error(interaction, error):
    if error == "You are missing Administrator permission(s) to run this command.":
        await interaction.response.send_message(content=error)
    else:
        raise error


@client.event
async def on_raw_reaction_add(payload):
    curriServer = ServerData[str(payload.guild_id)]
    currentEmoji = str(payload.emoji)
    if currentEmoji in curriServer[3]:
        channelToSendID = curriServer[0]
        run = True

        if not channelToSendID:
            run = False  # if setup not done then abort
        if payload.channel_id == channelToSendID:
            run = False

        ListOfStarBoardMessages = StarData[str(payload.guild_id)]

        if run:
            for ara in ListOfStarBoardMessages:
                if payload.message_id == ara:
                    run = False
                    break
                else:
                    continue

        if run:
            try:
                channelToSend = client.get_channel(channelToSendID)

                if not channelToSend:  # if channel got deleted
                    curriServer[0] = None
                    ServerData.update({str(payload.guild_id): curriServer})
                    with open("graphMods/dcData.json", mode="w") as araFile:
                        json.dump(ServerData, araFile, indent=4)
                    updater()
                    raise ValueError("channel deleted")

                channelThatgotReaction = client.get_channel(payload.channel_id)
                messageThatGotReaction = await channelThatgotReaction.fetch_message(payload.message_id)

                for ara in messageThatGotReaction.reactions:
                    if str(ara.emoji) != currentEmoji:
                        continue  # if not skull then skip
                    if ara.count >= curriServer[4]:
                        if messageThatGotReaction.attachments:
                            kawaiEmbed = discord.Embed(
                                type="image", description=messageThatGotReaction.content,
                                timestamp=messageThatGotReaction.created_at)
                            kawaiEmbed.set_image(
                                url=messageThatGotReaction.attachments[0].url)
                        else:
                            kawaiEmbed = discord.Embed(
                                description=messageThatGotReaction.content, timestamp=messageThatGotReaction.created_at)
                        try:
                            kawaiEmbed.set_author(
                                name=messageThatGotReaction.author.display_name,
                                icon_url=messageThatGotReaction.author.avatar.url)
                        except AttributeError:
                            kawaiEmbed.set_author(
                                name=messageThatGotReaction.author.display_name)
                        butaButton = discord.ui.Button(
                            label="Jump!", emoji=currentEmoji, style=discord.ButtonStyle.url,
                            url=messageThatGotReaction.jump_url)
                        tfIsView = discord.ui.View().add_item(butaButton)
                        await channelToSend.send(content=f"<#{payload.channel_id}>", embed=kawaiEmbed, view=tfIsView)
                        ListOfStarBoardMessages.append(payload.message_id)
                        StarData.update(
                            {str(payload.guild_id): ListOfStarBoardMessages})
                        with open("graphMods/starloglol.json", mode="w") as ranaTigrina:
                            json.dump(StarData, ranaTigrina, indent=4)
                        updater(mode=2)
            except ValueError:
                pass
