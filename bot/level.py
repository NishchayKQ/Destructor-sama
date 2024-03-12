import time
from io import BytesIO

import discord.interactions
from PIL import Image

from data import alphaDict
from setup import *
from utility import getLevel, convert_sec_to_day


def alphToImgConvertor(word, size: tuple[int, int] = (100, 56)) -> Image:
    word = str(word)
    alphabetOriginal = Image.open("graphMods/latest.jpg")
    word = word.lower()
    combo = []
    for ara in word:
        try:
            combo.append(alphaDict[ara])
        except KeyError:
            combo.append(alphaDict[" "])
            # handler.emit(f"char not in alphabetOriginal {ara}, from username {word}")
            print(f"bad char {ara}")

    if len(combo) == 1:
        toSend = alphabetOriginal.crop(combo[0])
        toSend.thumbnail(size)
        return toSend
    else:
        # different ways, if u use thumbnail before merging size is unknown(can be as wide as u want) but if you use
        # thumbnail in the end then size is fixed. test whichever is the best
        imgWidth = 0
        high = 0
        for ara in combo:
            temp = alphabetOriginal.crop(ara)
            temp.thumbnail(size)
            imgWidth = imgWidth + temp.size[0]
            if temp.size[1] > high:
                high = temp.size[1]
        # print(f"using width {imgWidth} and height {high}")
        toSend = Image.new("RGBA", (imgWidth, high))

        WidthTaken = 0
        for ara in combo:
            temp = alphabetOriginal.crop(ara)
            temp.thumbnail(size)
            toSend.paste(temp, (WidthTaken, 0))
            WidthTaken = WidthTaken + temp.size[0]

        # toSend.thumbnail(size)
        return toSend


# returns discord image file
async def rankCardMaker(
        author: discord.User,
        xp: int,
        level: int = None,
        size: tuple[int, int] = None,
        secs: int = None,
        mode: str = "on"
):
    MainBack = Image.open("graphMods/blackBack.jpg")
    if author.avatar:
        avatar_bytes = await author.avatar.read()
        # circleForAv = Image.open("graphMods/forav.png")
        profilePic = Image.open(BytesIO(avatar_bytes))
        # profilePic.save("graphMods/testing/out.gif")

        profilePic.thumbnail((128, 128))
        # profilePic.paste(circleForAv)
        MainBack.paste(profilePic, (106, 20))

        # MainBack.paste()
    if not level:
        level = getLevel(xp)
    MainBack.paste(alphToImgConvertor(level[0]), (754, 106))
    MainBack.paste(alphToImgConvertor(f"{xp} of {level[1]}"), (754, 235))

    if secs and level[0] != 0:
        MainBack.paste(alphToImgConvertor(
            f"{f'lev {level[0]} for {convert_sec_to_day(secs)}' if mode == 'on' else f'took them {convert_sec_to_day(secs)} to level up!'}",
            size=(700, 28)), (10, 285))
    MainBack.paste(alphToImgConvertor(str(author)), (106, 158))

    with BytesIO() as image_binary:
        MainBack.save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename='image.png')


@tree.command(name="setup_leveling",
              description="simple leveling feature! |passing no arguments will disable this feature",
              guilds=convertedGuilds)
@discord.app_commands.checks.has_permissions(administrator=True)
@discord.app_commands.describe(which_channel="channel where level updates get annouced!")
async def LevSet(interaction: discord.Interaction, which_channel: discord.TextChannel):
    particularServerData = {
        "channel": which_channel.id, "global": 1, "members": {}}
    LevelData.update({str(interaction.guild_id): particularServerData})
    ServerData[str(interaction.guild_id)][5] = True

    with open("graphMods/dcData.json", mode="w") as cafFile:
        json.dump(ServerData, cafFile, indent=4)
    with open("graphMods/level.json", mode="w") as araFile:
        json.dump(LevelData, araFile, indent=4)
    updater(mode=3)
    await interaction.response.send_message(content="okie dokie")


@tree.command(name="level", description="shows your level. Leave the user argument empty to see your own!",
              guilds=convertedGuilds)
@discord.app_commands.describe(user="The user who's level you want to see.")
async def myLevel(interaction: discord.Interaction, user: discord.User = None):
    author = interaction.user
    if user:
        author = user

    if not ServerData[str(interaction.guild_id)][5]:
        await interaction.response.send_message(
            content="leveling up isnt enabled on this server, try asking an Admin to run /setup_leveling ! #Nish make "
                    "this clickable")
    elif user and user.bot:
        await interaction.response.send_message(content="this user is a bot!")
    else:
        await interaction.response.defer()
        particularServerData = LevelData[str(interaction.guild_id)]
        personsData = particularServerData["members"].get(
            str(author.id), "new")
        if user:
            if not interaction.guild.get_member(author.id) and personsData == "new":
                await interaction.followup.send(
                    content="that user isnt on this server and has not sent a message while my leveling was active!")
            elif personsData == "new":
                personsData = [0, 0, 0, time.time()]
                particularServerData["members"].update(
                    {str(author.id): personsData})
                LevelData.update(
                    {str(interaction.guild_id): particularServerData})
                updater(mode=None, update_level=LevelData)

                file = await rankCardMaker(author=author, xp=personsData[0])
                await interaction.followup.send(file=file)
            else:
                file = await rankCardMaker(author=author, xp=personsData[0], secs=time.time() - personsData[3])
                await interaction.followup.send(file=file)
        elif personsData == "new":
            personsData = [0, 0, 0, time.time()]
            particularServerData["members"].update(
                {str(author.id): personsData})
            LevelData.update({str(interaction.guild_id): particularServerData})
            updater(mode=None, update_level=LevelData)

            file = await rankCardMaker(author=author, xp=personsData[0])
            await interaction.followup.send(file=file)
        else:

            file = await rankCardMaker(author=author, xp=personsData[0], secs=time.time() - personsData[3])
            await interaction.followup.send(file=file)


async def on_message_increase_xp(message: discord.Message, author: discord.User = None):
    # as xp is globalMulti*xp & xp is one so 1 is not needed
    particularServerData = LevelData[str(message.guild.id)]
    globalMulti = particularServerData["global"]
    if not author:
        author = message.author
    curriPerson = particularServerData["members"].get(
        str(author.id), "new")
    if curriPerson == "new":
        curriPerson = [globalMulti, time.time(), getLevel(globalMulti)[
            0], time.time()]
        particularServerData["members"].update(
            {str(author.id): curriPerson})
        LevelData.update({str(message.guild.id): particularServerData})
        updater(mode=None, update_level=LevelData)

    if (time.time() - curriPerson[1]) >= 8:
        curriPerson[0] = curriPerson[0] + globalMulti
        temp = getLevel(curriPerson[0])
        levelForCurrentXp = temp[0]
        if curriPerson[2] != levelForCurrentXp:
            channelToSend = client.get_channel(
                particularServerData["channel"])
            file = await rankCardMaker(author=author, xp=curriPerson[0], level=temp,
                                       secs=time.time() - curriPerson[3], mode="up")
            await channelToSend.send(content=f"<@{author.id}>", file=file)
            curriPerson[2] = levelForCurrentXp
            curriPerson[3] = time.time()

        particularServerData["members"].update({str(author.id): [
            curriPerson[0], time.time(), levelForCurrentXp, curriPerson[3]]})
        LevelData.update({str(message.guild.id): particularServerData})
        updater(mode=None, update_level=LevelData)
