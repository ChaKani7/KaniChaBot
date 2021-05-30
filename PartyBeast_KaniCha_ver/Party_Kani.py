import discord
import discord.guild
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
import asyncio
from datetime import datetime, timedelta
import os

bot = commands.Bot(command_prefix='&')
bot.remove_command("help")

guild_role = {}

voice_per = {}

@bot.event
async def on_ready():
    guild_list = bot.guilds

    for guild in guild_list:
        guild_role[guild.id] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 26):
            guild_role[guild.id][i] = chr(65+i)

    game = discord.Game(f'&start_system')
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_voice_state_update(member, before, after):
    server = member.guild
    server_id = member.guild.id

    f = open(f"[Location]\guild_list\{server_id}.txt", 'r')
    cat_id, voice_chn_id = f.read().split('\n')
    cat_id = int(cat_id)
    voice_chn_id = int(voice_chn_id)
    f.close()

    cat = bot.get_channel(cat_id)

    if after.channel == None:
        if len(before.channel.members) == 0 and cat == before.channel.category and before.channel.id != voice_chn_id:
            await before.channel.delete()
            await voice_per[before.channel.id].delete()
            t = ord(voice_per[before.channel.id].name)
            guild_role[server_id][t-65] = chr(t)
            del voice_per[before.channel.id]
            return None

        elif cat == before.channel.category and before.channel.id != voice_chn_id:
            await member.remove_roles(voice_per[before.channel.id])
            return None

    if after.channel.id == voice_chn_id and before.channel == None:
        voice_channel = await server.create_voice_channel(f'{member.name}\'s room', category=cat, overwrites=None, reason=None, bitrate = 96000)
        for i in range(0, 26):
            if guild_role[server_id][i] != 0:
                temp = guild_role[server_id][i]
                guild_role[server_id][i] = 0
                break

        role = await server.create_role(name=f"{temp}")
        voice_per[voice_channel.id] = role
        await member.add_roles(role)
        await member.move_to(voice_channel)
        await voice_channel.set_permissions(role, manage_channels=True)
        return None

    elif after.channel.id == voice_chn_id and cat == before.channel.category:
        if len(before.channel.members) == 0:
            await before.channel.delete()
            await voice_per[before.channel.id].delete()
            t = ord(voice_per[before.channel.id].name)
            guild_role[server_id][t-65] = chr(t)
            del voice_per[before.channel.id]
        else:
            await member.remove_roles(voice_per[before.channel.id])

        voice_channel = await server.create_voice_channel(f'{member.name}\'s room', category=cat, overwrites=None, reason=None, bitrate = 96000)
        for i in range(0, 26):
            if guild_role[server_id][i] != 0:
                temp = guild_role[server_id][i]
                guild_role[server_id][i] = 0
                break

        role = await server.create_role(name=f"{temp}")
        voice_per[voice_channel.id] = role
        await member.add_roles(role)
        await member.move_to(voice_channel)
        await voice_channel.set_permissions(role, manage_channels=True)
        return None

    elif after.channel.id == voice_chn_id:
        voice_channel = await server.create_voice_channel(f'{member.name}\'s room', category=cat, overwrites=None, reason=None, bitrate = 96000)
        for i in range(0, 26):
            if guild_role[server_id][i] != 0:
                temp = guild_role[server_id][i]
                guild_role[server_id][i] = 0
                break

        role = await server.create_role(name=f"{temp}")
        voice_per[voice_channel.id] = role
        await member.add_roles(role)
        await member.move_to(voice_channel)
        await voice_channel.set_permissions(role, manage_channels=True)
        return None
    
    if cat == after.channel.category and after.channel.id != voice_chn_id and before.channel == None:
        await member.add_roles(voice_per[after.channel.id])
        return None

    elif cat == after.channel.category and after.channel.id != voice_chn_id:
        if len(before.channel.members) == 0 and before.channel.id != voice_chn_id and cat == before.channel.category:
            await before.channel.delete()
            await voice_per[before.channel.id].delete()
            t = ord(voice_per[before.channel.id].name)
            guild_role[server_id][t-65] = chr(t)
            del voice_per[before.channel.id]
        elif before.channel.id != voice_chn_id and cat == before.channel.category:
            await member.remove_roles(voice_per[before.channel.id])

        await member.add_roles(voice_per[after.channel.id])
        return None

    if len(before.channel.members) == 0 and cat == before.channel.category and before.channel.id != voice_chn_id and after.channel == None:
        await before.channel.delete()
        await voice_per[before.channel.id].delete()
        t = ord(voice_per[before.channel.id].name)
        guild_role[server_id][t-65] = chr(t)
        t = 0
        del voice_per[before.channel.id]
        return None

    elif len(before.channel.members) == 0 and cat == before.channel.category and before.channel.id != voice_chn_id:
        await before.channel.delete()
        await voice_per[before.channel.id].delete()
        t = ord(voice_per[before.channel.id].name)
        guild_role[server_id][t-65] = chr(t)
        t = 0
        del voice_per[before.channel.id]
        return None

    if cat == before.channel.category and before.channel.id != voice_chn_id and after.channel == None:
        await member.remove_roles(voice_per[before.channel.id])
        return None

    elif cat == before.channel.category and before.channel.id != voice_chn_id:
        await member.remove_roles(voice_per[before.channel.id])
        return None


@bot.command()
async def start_system(ctx):
    path = "[Location]\guild_list"
    file_list = os.listdir(path)

    if f'{ctx.guild.id}.txt' in file_list:
        await ctx.send('このサーバーはすでに初期設定が終わっています！')
    else:
        server = ctx.guild
        server_id = ctx.guild.id
        await ctx.send('初期設定を行います！')
        category = await server.create_category('KaniChaBot Category', overwrites=None, reason=None)
        voice_channel = await server.create_voice_channel('クリック｜클릭！', category=category, overwrites=None, reason=None, bitrate = 96000)
        f = open(f"[Location]\guild_list\{server_id}.txt", 'w')
        f.write(str(category.id) + '\n' + str(voice_channel.id))
        f.close()

bot.run("[Discord Bot Token]")