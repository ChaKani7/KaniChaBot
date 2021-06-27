import discord
import discord.guild
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='&')
bot.remove_command("help")

guild_role = {}

vcRole = {}

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was successful')

    guild_list = bot.guilds
    for i in guild_list:
        print("Server ID: {0} / Server Name: {1}".format(i.id, i.name))
        
    for guild in guild_list:
        guild_role[guild.id] = []

    game = discord.Game(f'&help')
    await bot.change_presence(status=discord.Status.online, activity=game)

async def createChannel(server, server_id, member, category):
    voice_channel = await server.create_voice_channel(f'{member.name}の部屋！', category=category, overwrites=None, reason=None, bitrate = 96000)
        
    i = 0
    while True:
        if i not in guild_role[server_id]:
            guild_role[server_id].append(i)
            break
        i += 1

    role = await server.create_role(name=f"VC{i}")
    vcRole[voice_channel.id] = role
    await member.add_roles(role)
    await member.move_to(voice_channel)
    await voice_channel.set_permissions(role, manage_channels=True)

async def deleteChannelandRole(server_id, before):
    await before.channel.delete()
    await vcRole[before.channel.id].delete()
    guild_role[server_id].remove(int(vcRole[before.channel.id].name[2:]))
    del vcRole[before.channel.id]

@bot.event
async def on_voice_state_update(member, before, after):
    try:
        server = member.guild
        server_id = member.guild.id

        path = r"[PATH]/guild_list"
        
        fileCheckBoolean = False
        for file in os.listdir(path):
            if file == f'{server_id}.txt':
                fileCheckBoolean = True
                break

        if fileCheckBoolean == False:
            return None
        
        f = open(f"[PATH]/guild_list/{server_id}.txt", 'r')
        categoryID, clickID = f.read().split('\n')
        categoryID = int(categoryID)
        clickID = int(clickID)
        f.close()

        category = bot.get_channel(categoryID)

        if before.channel == None or before.channel.id not in vcRole:
            if after.channel != None:
                if after.channel.category == category:
                    if after.channel.id == clickID:
                        await createChannel(server, server_id, member, category)
                        return None
                    elif after.channel.id != clickID:
                        await member.add_roles(vcRole[after.channel.id])
                        return None
                    else:
                        return None
                elif after.channel.category != category:
                    return None
                else:
                    return None
            elif after.channel == None:
                return None
                
        elif before.channel != None:
            if after.channel == None:
                if before.channel.category == category:
                    if len(before.channel.members) == 0:
                        await deleteChannelandRole(server_id, before)
                        return None
                    await member.remove_roles(vcRole[before.channel.id])
                    return None
                else:
                    return None
            elif after.channel != None:
                if before.channel.category == category:
                    if after.channel.category == category:
                        if after.channel.id == clickID:
                            if len(before.channel.members) == 0:
                                await deleteChannelandRole(server_id, before)
                                await createChannel(server, server_id, member, category)
                                return None
                            await member.remove_roles(vcRole[before.channel.id])
                            await createChannel(server, server_id, member, category)
                            return None
                        elif after.channel.id != clickID:
                            if len(before.channel.members) == 0:
                                await deleteChannelandRole(server_id, before)
                                await member.add_roles(vcRole[after.channel.id])
                                return None
                            await member.remove_roles(vcRole[before.channel.id])
                            await member.add_roles(vcRole[after.channel.id])
                            return None
                    elif after.channel.category != category:
                        if len(before.channel.members) == 0:
                            await deleteChannelandRole(server_id, before)
                            return None
                        await member.remove_roles(vcRole[before.channel.id])
                        return None
                    else:
                        return None
                elif before.channel.category != category:
                    if after.channel.category == category:
                        if after.channel.id == clickID:
                            await createChannel(server, server_id, member, category)
                            return None
                        elif after.channel.id != clickID:
                            await member.add_roles(vcRole[after.channel.id])
                            return None
                    elif after.channel.category != category:
                        return None
                else:
                    return None
    except Exception as e:
        print('Error!', e)
        return None
    

@bot.command()
async def test(ctx):
    for channel in ctx.guild.channels:
        print(channel.id)
    return None

async def initialize(ctx, server, server_id):
    await ctx.send('初期設定を行います！')
    category = await server.create_category('KaniChaBot Category', overwrites=None, reason=None)
    voice_channel = await server.create_voice_channel('クリック｜클릭！', category=category, overwrites=None, reason=None, bitrate = 96000)
    f = open(f"[PATH]/guild_list/{server_id}.txt", 'w')
    f.write(str(category.id) + '\n' + str(voice_channel.id))
    f.close()
    guild_role[server_id] = []

@bot.command()
async def start_system(ctx):
    server = ctx.guild
    server_id = ctx.guild.id
    
    path = "[PATH]/guild_list"
    file_list = os.listdir(path)

    if f'{ctx.guild.id}.txt' in file_list:
        f = open(f"[PATH]/guild_list/{server_id}.txt", 'r')
        categoryID, clickID = f.read().split('\n')
        categoryID = int(categoryID)
        clickID = int(clickID)
        f.close()
        
        channelIdList = []
        for channel in ctx.guild.channels:
            channelIdList.append(channel.id)
        
        if categoryID in channelIdList and clickID in channelIdList:
            if channelIdList.index(clickID)-1 == channelIdList.index(categoryID):
                await ctx.send('このサーバーはすでに初期設定が終わっています！')
            else:
                await initialize(ctx, server, server_id)
        else:
            await initialize(ctx, server, server_id)

    else:
        await initialize(ctx, server, server_id)
    
    return None
        
@bot.command()
async def start_system_ignore(ctx):
    server = ctx.guild
    server_id = ctx.guild.id
    
    await initialize(ctx, server, server_id)
    
    return None

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="PartyBeast_KaniCha_ver's Commands", color=0xf5c2d6)
    embed.add_field(name="&start_system", value="このサーバーについてのBOTの初期設定を行います！\n이 서버에 대한 봇의 초기설정을 수행합니다!", inline=False)
    embed.add_field(name="&start_system_ignore", value="なにかの問題があった場合このコマンドを入力して再設定してください！\n어떠한 문제가 발생하였을 시 이 명령어를 입력하여 재설정해주세요!", inline=False)
    embed.set_footer(text="PartyBeast_KaniCha_ver", icon_url="https://i.imgur.com/OaJGIpi.png")
    embed.set_thumbnail(url="https://i.imgur.com/OaJGIpi.png")
    await ctx.channel.send(embed=embed)

bot.run("[Discord Bot Token]")
