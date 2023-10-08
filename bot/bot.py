# Note all dictionary keys are strings as json doesnt support integer keys
# using all intents rn u check if thats needed
# https://gist.github.com/lykn/bac99b06d45ff8eed34c2220d86b6bf4 button help
# m & s forum
"""
for dcData.json is single dict with list as value of keys
key will be server id, {serverid:[skullboard,delas-delete,vipChannel,💀,no of reactions,levelUpOn]

for starloglol.json
key will be server id, {serverid:[list of message ids]
"""

import discord
import logging
import json
import time
from math import sqrt, floor, ceil
from PIL import Image
from io import BytesIO

disconnectTime = None

with open("graphMods/dcData.json") as araFile:
    ServerData = json.load(araFile)
with open("graphMods/starloglol.json") as knyaFile:
    starData = json.load(knyaFile)
with open("graphMods/level.json") as frenchFile:
    levelData = json.load(frenchFile)

owner = []  # List of owner IDs
listOfServers = []  # id of servers you want the bot to work in
channelID = 0  # Channel ID the bot will post if its online!
token = ''  # add your token


convertedGuilds = []
for ara in listOfServers:
    convertedGuilds.append(discord.Object(id=ara))


def ConvertSectoDay(n):
    n = floor(n)
    day = n // (24 * 3600)
    n = n % (24 * 3600)
    hour = n // 3600
    n %= 3600
    minutes = n // 60
    n %= 60
    seconds = n

    return (f"{f'{day} days ' if day else ''}{f'{hour} hours ' if hour else ''}{f'{minutes} minutes ' if minutes else ''}{'' if (not day and not hour and not minutes) or (not seconds) else 'and '}{f'{seconds} seconds' if seconds else ''}")


def amPamConverter(Received, mode=1):
    if mode == 1:  # Received is string here
        H, m = Received.split()
        H = int(H)
        if H > 12:
            H = H - 12
            amPam = "pm"
        else:
            amPam = "am"
        return f"{H}:{m} {amPam}"
    if mode == 2:  # Received is like ["19 00 - 19 40\n" , "20 00 - 21 00\n" ]
        culturedList = []
        for amoeba in Received:
            am1 = "am"
            am2 = "am"
            nLessAmoeba = amoeba[:-1]
            init_timestamp, final_timeStamp = nLessAmoeba.split(" - ")
            # h1,m1,am1          h2 m2,am2
            h1, m1 = init_timestamp.split()
            h2, m2 = final_timeStamp.split()
            h1 = int(h1)
            h2 = int(h2)
            if h1 > 12:
                h1 = h1 - 12
                am1 = "pm"
            if h2 > 12:
                h2 = h2 - 12
                am2 = "pm"
            culturedList.append(f"{h1}:{m1} {am1} - {h2}:{m2} {am2}\n")
        return culturedList


def upDater(mode=1, updateLevel=None):
    global ServerData, starData, levelData
    if mode == 1:  # default mode which is to update ServerData
        with open("graphMods/dcData.json") as araFile:
            ServerData = json.load(araFile)
    elif updateLevel:
        with open("graphMods/level.json", mode="w") as ireFile:
            json.dump(updateLevel, ireFile)
        # with open("graphMods/level.json") as araFile:
        #   levelData = json.load(araFile)
        levelData = updateLevel
        # print(f" from upDater {levelData}")
    else:  # update all usually i use mode 2 for this
        with open("graphMods/dcData.json") as araFile:
            ServerData = json.load(araFile)
        with open("graphMods/starloglol.json") as knyaFile:
            starData = json.load(knyaFile)
        with open("graphMods/level.json") as araFile:
            levelData = json.load(araFile)


def getLevel(xp):
    if xp <= 34:  # for level 0 no formula
        return (0, 35)
    else:
        calcu = 1 + (sqrt(5*(xp - 35)))/10
        x = ceil(calcu)
        y = (20*(x*x)) - (40*(x)) + 55
        return (floor(calcu), y)


handler = logging.FileHandler(
    filename='graphMods/discord.log', encoding='utf-8', mode='w')


alphaDict = {
    "a": (42, 206, 98, 285),
    "b": (109, 206, 152, 285),
    "c": (165, 206, 210, 285),
    "d": (229, 206, 284, 285),
    "e": (291, 206, 330, 285),
    "f": (339, 206, 372, 285),
    "g": (377, 206, 426, 285),
    "h": (438, 206, 474, 285),
    "i": (490, 206, 503, 285),
    "j": (512, 206, 541, 285),
    "k": (554, 206, 592, 285),
    "l": (607, 206, 646, 285),
    "m": (660, 206, 717, 285),
    "n": (726, 206, 777, 285),
    "o": (790, 206, 830, 285),
    "p": (851, 206, 895, 285),
    "q": (903, 206, 968, 285),
    "r": (977, 206, 1038, 285),
    "s": (1041, 206, 1079, 285),
    "t": (1090, 206, 1135, 285),
    "u": (48, 307, 109, 386),
    "v": (110, 307, 153, 386),
    "w": (163, 307, 229, 386),
    "x": (240, 307, 295, 386),
    "y": (301, 307, 344, 386),
    "z": (354, 307, 403, 386),
    "1": (572, 307, 583, 386),
    "2": (596, 307, 636, 386),
    "3": (646, 307, 687, 386),
    "4": (696, 307, 741, 386),
    "5": (745, 307, 786, 386),
    "6": (798, 307, 834, 386),
    "7": (844, 307, 879, 386),
    "8": (885, 307, 920, 386),
    "9": (928, 307, 961, 386),
    "0": (972, 307, 1006, 386),
    ".": (421, 307, 437, 386),
    "_": (453, 307, 493, 386),
    " ": (527, 307, 569, 386), }


def alphToImgConvertor(word, size=(100, 56)):
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
        # different ways, if u use thumbnail before merging size is unknown(can be as wide as u want) but if you use thumbnail in the end then size is fixed.
        # test whichever is the best
        imgWidth = 0
        high = 0
        for ara in combo:
            temp = alphabetOriginal.crop(ara)
            temp.thumbnail(size)
            imgWidth = imgWidth + temp.size[0]
            if temp.size[1] > high:
                high = temp.size[1]
        # print(f"using width {imgWidth} and hight {high}")
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
async def rankCardMaker(author, xp, level=None, size=None, secs=None, mode="on"):
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
            f"{f'lev {level[0]} for {ConvertSectoDay(secs)}' if mode == 'on' else f'took them {ConvertSectoDay(secs)} to level up!'}", size=(700, 28)), (10, 285))
    MainBack.paste(alphToImgConvertor(str(author)), (106, 158))

    with BytesIO() as image_binary:
        MainBack.save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename='image.png')


intents = discord.Intents.all()
# intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f'destructor Sama has awoken {client.user}')
    for ara in listOfServers:
        await tree.sync(guild=discord.Object(id=ara))
    # await tree.sync(guild=discord.Object(id=724927091971194970))
    # await tree.sync(guild=discord.Object(id=1134235922301468712))
    if channelID:
        channelToSend = client.get_channel(channelID)
    # channelToSend = client.get_channel(1134238470131433474)
        global disconnectTime

        current_time = time.localtime()
        if disconnectTime:
            ConnectTime = time.strftime("%H %M\n", current_time)
            timeLog = [disconnectTime + ConnectTime]
            await channelToSend.send(f"{amPamConverter(timeLog,mode = 2)} ready for destruction!")
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
        json.dump(ServerData, ranaTigrina)
    with open("graphMods/starloglol.json", mode="w") as OceanMan:
        starData.update({str(guild.id): []})
        json.dump(starData, OceanMan)
    upDater(mode=2)


@client.event
async def on_guild_remove(guild):
    with open("graphMods/dcData.json", mode="w") as ranaTigrina:
        ServerData.pop(str(guild.id))
        json.dump(ServerData, ranaTigrina)
    with open("graphMods/starloglol.json", mode="w") as OceanMan:
        starData.pop(str(guild.id))
        json.dump(starData, OceanMan)
    upDater(mode=2)


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Button", style=discord.ButtonStyle.primary)
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await interaction.response.edit_message(content="This is an edited button response!")


@tree.command(name="rockpapersizzler", description="what do u mean \"wtf is this command?\"", guilds=convertedGuilds)
async def rpc(interaction: discord.Interaction):
    badboisEmbed = discord.Embed(
        title=f"{interaction.user.display_name}'s game of rpc", description="insert something")

    # butaButton = discord.ui.Button(label = "1",style = discord.ButtonStyle.primary,custom_id = "one")
    # tfIsView = discord.ui.View().add_item(butaButton)
    await interaction.response.send_message(embed=badboisEmbed, view=Buttons())


@tree.command(name="say", description="Constructor-Sama Can speak!", guilds=convertedGuilds)
async def sayStuff(interaction: discord.Interaction, what_to_say: str, which_channel: discord.TextChannel = None):
    if interaction.user.id in owner:
        if not which_channel:
            which_channel = interaction.channel
        await which_channel.send(content=what_to_say)
        await interaction.response.send_message(content="oki dokie", ephemeral=True)
        await interaction.delete_original_response()
    else:
        await interaction.response.send_message(content="only KepKep can make me say stuff!", ephemeral=True)


@tree.command(name="setup_skullboard", description="manage or add skullboard | passing no arguments will disable this feature", guilds=convertedGuilds)
@discord.app_commands.checks.has_permissions(administrator=True)
@discord.app_commands.describe(emojis="can enter multiple, only recognises gold variant for coloured emojis like 👍👍🏽")
@discord.app_commands.describe(channel="channel where destructor will post in")
@discord.app_commands.describe(number_of_reactions="no. of reactions for a message to get posted in skullboard...default is 3")
async def skullSet(interaction: discord.Interaction, channel: discord.TextChannel = None, emojis: str = None, number_of_reactions: int = None):
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
            json.dump(ServerData, araFile)
        upDater()
    except discord.errors.HTTPException:
        await interaction.channel.send(content="emoji not found")


@tree.command(name="setup_delas-delete", description="channel where deleted messages go | passing no arguments will disable this feature", guilds=convertedGuilds)
@discord.app_commands.checks.has_permissions(administrator=True)
async def delSet(interaction: discord.Interaction, which_channel: discord.TextChannel = None):
    particularServerData = ServerData[str(interaction.guild_id)]
    if which_channel:
        particularServerData[1] = which_channel.id
    else:
        particularServerData[1] = None
    ServerData.update({str(interaction.guild_id): particularServerData})
    with open("graphMods/dcData.json", mode="w") as araFile:
        json.dump(ServerData, araFile)
    upDater()
    await interaction.response.send_message(content="okie dokie")


@tree.command(name="setup_leveling", description="simple leveling feature! |passing no arguments will disable this feature", guilds=convertedGuilds)
@discord.app_commands.checks.has_permissions(administrator=True)
@discord.app_commands.describe(which_channel="channel where level updates get annouced!")
async def LevSet(interaction: discord.Interaction, which_channel: discord.TextChannel):
    particularServerData = {
        "channel": which_channel.id, "global": 1, "members": {}}
    levelData.update({str(interaction.guild_id): particularServerData})
    ServerData[str(interaction.guild_id)][5] = True

    with open("graphMods/dcData.json", mode="w") as cafFile:
        json.dump(ServerData, cafFile)
    with open("graphMods/level.json", mode="w") as araFile:
        json.dump(levelData, araFile)
    upDater(mode=3)
    await interaction.response.send_message(content="okie dokie")


@delSet.error
async def delSet_error(interaction, error):
    if error == "You are missing Administrator permission(s) to run this command.":
        await interaction.response.send_message(content=error)
    else:
        raise error


@skullSet.error
async def skullSet_error(interaction, error):
    if error == "You are missing Administrator permission(s) to run this command.":
        await interaction.response.send_message(content=error)
    else:
        raise error


@tree.command(name="level", description="shows your level. Leave the user argument empty to see your own!", guilds=convertedGuilds)
@discord.app_commands.describe(user="The user who's level you want to see.")
async def myLevel(interaction: discord.Interaction, user: discord.User = None):
    author = interaction.user
    if user:
        author = user

    if not ServerData[str(interaction.guild_id)][5]:
        await interaction.response.send_message(content="leveling up isnt enabled on this server, try asking an Admin to run /setup_leveling ! #Nish make this clickable")
    elif user and user.bot:
        await interaction.response.send_message(content="this user is a bot!")
    else:
        await interaction.response.defer()
        particularServerData = levelData[str(interaction.guild_id)]
        personsData = particularServerData["members"].get(
            str(author.id), "new")
        if user:
            if not interaction.guild.get_member(author.id) and personsData == "new":
                await interaction.followup.send(content="that user isnt on this server and has not sent a message while my leveling was active!")
            elif personsData == "new":
                personsData = [0, 0, 0, time.time()]
                particularServerData["members"].update(
                    {str(author.id): personsData})
                levelData.update(
                    {str(interaction.guild_id): particularServerData})
                upDater(mode=None, updateLevel=levelData)

                file = await rankCardMaker(author=author, xp=personsData[0])
                await interaction.followup.send(file=file)
            else:
                file = await rankCardMaker(author=author, xp=personsData[0], secs=time.time() - personsData[3])
                await interaction.followup.send(file=file)
        elif personsData == "new":
            personsData = [0, 0, 0, time.time()]
            particularServerData["members"].update(
                {str(author.id): personsData})
            levelData.update({str(interaction.guild_id): particularServerData})
            upDater(mode=None, updateLevel=levelData)

            file = await rankCardMaker(author=author, xp=personsData[0])
            await interaction.followup.send(file=file)
        else:

            file = await rankCardMaker(author=author, xp=personsData[0], secs=time.time() - personsData[3])
            await interaction.followup.send(file=file)


@tree.context_menu(name="bookmark a message", guilds=convertedGuilds)
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
async def on_raw_message_delete(message):
    channelToSendID = None
    if message.guild_id:  # haha if message is ephemeral or dm message delete then ignore
        channelToSendID = ServerData[str(message.guild_id)][1]
    if channelToSendID:
        try:
            if message.channel_id == channelToSendID:
                raise AttributeError("not this channel lmao")
            if message.cached_message.author.id in owner:  # was messging around when i added this...remove it
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
                    json.dump(ServerData, araFile)
                upDater()
                raise AttributeError("channel deleted")
            await channelToSend.send(embed=kawaiestEmbed)
        except AttributeError:
            pass


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # if message.content.startswith('say ')

    if message.content.startswith('venus'):
        await message.channel.send('Love is show! Misetekure~')

    """
  if message.content.startswith('c ch make'):
      try:
        with open("graphMods/dcData.json") as araFile:
          FileData = json.load(araFile)
        categoryID = FileData[str(message.guild.id)]
      except KeyError:
        await message.reply("Server setup not done yet, try running `c ch setup` first")
      else:
        
        try:
          ownerIs = message.mentions
          if not ownerIs: raise ValueError("no owners provided")
          nameOfChannel,roleName,owner = message.content[10:].split(",")
        except ValueError:
          await message.reply("mentions owners of the channel,follow the format `c ch make nameOfChannel,roleName,mentionTheOwner(s)`")
        else:
          new_role = await message.guild.create_role(name = roleName , reason = "channel create command")
          
          mergeThisDict = {}
          for ara in ownerIs:
            await ara.add_roles(new_role)
            mergeThisDict.update({ara:discord.PermissionOverwrite(manage_channels = True,manage_messages = True)})
            
          overwrites = {
          message.guild.default_role: discord.PermissionOverwrite(view_channel=False),
          new_role: discord.PermissionOverwrite(view_channel=True,external_emojis = True,read_message_history =True,add_reactions =True,send_messages = True,attach_files = True)}
          overwrites.update(mergeThisDict)
          new_channel = await message.guild.create_text_channel(name = nameOfChannel, category = discord.utils.get(message.guild.categories, id = categoryID),reason = "channel create command",overwrites = overwrites)
          
          for ara in ownerIs:
            await new_channel.send(f"<@{ara.id}>")
          
          await new_channel.send(f"yo! welcome to your new channel!")
  
  """
    if message.content.startswith('c sleep') and message.author.id in owner:
        await message.add_reaction("👍")
        await client.close()

    if message.content.startswith('cre') and message.author.id in owner:
        await message.add_reaction("👍")
        import os
        import sys
        os.execv(sys.executable, ['python'] + sys.argv)

    if message.guild and ServerData[str(message.guild.id)][5] and not message.author.bot:
        # as xp is globalMulti*xp & xp is one so 1 is not needed
        particularServerData = levelData[str(message.guild.id)]
        globalMulti = particularServerData["global"]
        curriPerson = particularServerData["members"].get(
            str(message.author.id), "new")
        if curriPerson == "new":
            curriPerson = [globalMulti, time.time(), getLevel(globalMulti)[
                0], time.time()]
            particularServerData["members"].update(
                {str(message.author.id): curriPerson})
            levelData.update({str(message.guild.id): particularServerData})
            upDater(mode=None, updateLevel=levelData)

        if (time.time() - curriPerson[1]) >= 8:
            curriPerson[0] = curriPerson[0] + globalMulti
            temp = getLevel(curriPerson[0])
            levelForCurrentXp = temp[0]
            if curriPerson[2] != levelForCurrentXp:
                channelToSend = client.get_channel(
                    particularServerData["channel"])
                file = await rankCardMaker(author=message.author, xp=curriPerson[0], level=temp, secs=time.time() - curriPerson[3], mode="up")
                await channelToSend.send(content=f"<@{message.author.id}>", file=file)
                curriPerson[2] = levelForCurrentXp
                curriPerson[3] = time.time()

            particularServerData["members"].update({str(message.author.id): [
                                                   curriPerson[0], time.time(), levelForCurrentXp, curriPerson[3]]})
            levelData.update({str(message.guild.id): particularServerData})
            upDater(mode=None, updateLevel=levelData)

    """
  if message.content.startswith('c ch setup'):
    try:
      serverID = str(message.guild.id)
      with open("graphMods/dcData.json") as araFile:
        FileData = json.load(araFile)
      
      if message.content.rstrip() == "c ch setup": raise ValueError("no arguments passed bruh")
    except ValueError:
      await message.reply("mention id of category")
    else:
      new_categoryID = int(message.content[10:].replace(" ",""))
      
      await message.reply(f"ok setting up <#{new_categoryID}> as vip category")
      
      FileData.update({serverID:new_categoryID})
      
      with open("graphMods/dcData.json",mode = "w") as baaFile:
        json.dump(FileData,baaFile)
  """

    """
  if message.content.startswith('c destroy'):
    try:
      if not message.mentions: raise ValueError("no mensions")
    except ValueError:
      member = await client.fetch_user(message.content[10:].rstrip())
      await message.guild.kick(member)
      await message.reply(f"destroyed {member.name}")
    else:
      boot = []
      for ara in message.mentions:
        await message.guild.kick(ara)
        boot.append(ara.name)
      await message.reply(f"destroyed {boot}")
  """


@client.event
async def on_raw_reaction_add(payload):
    Curriserver = ServerData[str(payload.guild_id)]
    currentEmoji = str(payload.emoji)
    if currentEmoji in Curriserver[3]:
        channelToSendID = Curriserver[0]
        run = True

        if not channelToSendID:
            run = False  # if setup not done then abort
        if payload.channel_id == channelToSendID:
            run = False

        ListOfStarBoardMessages = starData[str(payload.guild_id)]

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
                    Curriserver[0] = None
                    ServerData.update({str(payload.guild_id): Curriserver})
                    with open("graphMods/dcData.json", mode="w") as araFile:
                        json.dump(ServerData, araFile)
                    upDater()
                    raise ValueError("channel deleted")

                channelThatgotReaction = client.get_channel(payload.channel_id)
                messageThatGotReaction = await channelThatgotReaction.fetch_message(payload.message_id)

                for ara in messageThatGotReaction.reactions:
                    if str(ara.emoji) != currentEmoji:
                        continue  # if not skull then skip
                    if ara.count >= Curriserver[4]:
                        if messageThatGotReaction.attachments:
                            kawaiEmbed = discord.Embed(
                                type="image", description=messageThatGotReaction.content, timestamp=messageThatGotReaction.created_at)
                            kawaiEmbed.set_image(
                                url=messageThatGotReaction.attachments[0].url)
                        else:
                            kawaiEmbed = discord.Embed(
                                description=messageThatGotReaction.content, timestamp=messageThatGotReaction.created_at)
                        try:
                            kawaiEmbed.set_author(
                                name=messageThatGotReaction.author.display_name, icon_url=messageThatGotReaction.author.avatar.url)
                        except AttributeError:
                            kawaiEmbed.set_author(
                                name=messageThatGotReaction.author.display_name)
                        butaButton = discord.ui.Button(
                            label="Jump!", emoji=currentEmoji, style=discord.ButtonStyle.url, url=messageThatGotReaction.jump_url)
                        tfIsView = discord.ui.View().add_item(butaButton)
                        await channelToSend.send(content=f"<#{payload.channel_id}>", embed=kawaiEmbed, view=tfIsView)
                        ListOfStarBoardMessages.append(payload.message_id)
                        starData.update(
                            {str(payload.guild_id): ListOfStarBoardMessages})
                        with open("graphMods/starloglol.json", mode="w") as ranaTigrina:
                            json.dump(starData, ranaTigrina)
                        upDater(mode=2)
            except ValueError:
                pass

client.run(token,
           log_handler=handler)
