import discord
from discord.ext import commands
from discord.ext import tasks
from discord.reaction import Reaction
from discord.utils import get
import asyncio
import urllib.request
import fasttext
import re
from google.cloud import texttospeech
import nekos

import os
import sys
import time
import socket
import random
import asyncio

import requests
from bs4 import BeautifulSoup

from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError

from PIL import Image

intents = discord.Intents().default()
intents.members = True

bot = commands.Bot(command_prefix='^', intents = intents)
bot.remove_command("help")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="[Google API File Location]"

client = texttospeech.TextToSpeechClient()

v_client_id = "[Naver Client id]"
v_client_secret = "[Naver Client Secret]"

k_de = 'A'
j_de = 'B'

k_list = ['A', 'B', 'C', 'D']
j_list = ['A', 'B', 'C', 'D']

chnl = {}
k_koe = {}
j_koe = {}

voice = {}

channel_t = {}

@tasks.loop(seconds=1)
async def my_background_task():
    for key in list(voice.keys()):
        guild = bot.get_guild(key)
        name = [member.name for member in guild.voice_client.channel.members]
        if len(name) == 1:
            voice_client = guild.voice_client
            await channel_t[key].send("BOT DISCONNECT 完了（自動）")
            await voice_client.disconnect()
            del(voice[key])
            print(removeAllFile('[LOCATION]\TTS'))

@my_background_task.before_loop
async def before_my_task():
    await bot.wait_until_ready()


@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was successful')

    guild_list = bot.guilds
    for i in guild_list:
        print("Server ID: {0} / Server Name: {1}".format(i.id, i.name))

    game = discord.Game(f'^help | {len(bot.guilds)} servers')
    await bot.change_presence(status=discord.Status.online, activity=game)

    await my_background_task.start()

@bot.command()
async def 가위바위보(ctx, val):
    if val == '가위':
        COM_val = random.randrange(0, 3)

        if COM_val == 0:
            embed = discord.Embed(title="가위바위보", description="가위! 비겼어요!", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 1:
            embed = discord.Embed(title="가위바위보", description="바위! 제가 이겼어요!", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 2:
            embed = discord.Embed(title="가위바위보", description="보! 제가 졌어요!", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None

    elif val == '바위':
        COM_val = random.randrange(0, 3)

        if COM_val == 0:
            embed = discord.Embed(title="가위바위보", description="가위! 제가 졌어요!", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 1:
            embed = discord.Embed(title="가위바위보", description="바위! 비겼어요!", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 2:
            embed = discord.Embed(title="가위바위보", description="보! 제가 이겼어요!", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None

    elif val == '보':
        COM_val = random.randrange(0, 3)

        if COM_val == 0:
            embed = discord.Embed(title="가위바위보", description="가위! 제가 이겼어요!", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 1:
            embed = discord.Embed(title="가위바위보", description="바위! 제가 졌어요!", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 2:
            embed = discord.Embed(title="가위바위보", description="보! 비겼어요!", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None

    else:
        await ctx.send("<@{}> 가위, 바위, 보 중 하나를 입력해주세요!".format(ctx.author.id))
        return None

@bot.command()
async def じゃんけん(ctx, val):
    if val == 'チョキ':
        COM_val = random.randrange(0, 3)

        if COM_val == 0:
            embed = discord.Embed(title="じゃんけん", description="チョキ！あいこですね！", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 1:
            embed = discord.Embed(title="じゃんけん", description="グー！私が勝ちました！", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 2:
            embed = discord.Embed(title="가위바위보", description="パー！私が負けました！", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None

    elif val == 'グー':
        COM_val = random.randrange(0, 3)

        if COM_val == 0:
            embed = discord.Embed(title="じゃんけん", description="チョキ！私が負けました！", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 1:
            embed = discord.Embed(title="じゃんけん", description="グー！あいこですね！", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 2:
            embed = discord.Embed(title="じゃんけん", description="パー！私が勝ちました！", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None

    elif val == 'パー':
        COM_val = random.randrange(0, 3)

        if COM_val == 0:
            embed = discord.Embed(title="じゃんけん", description="チョキ！私が勝ちました！", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 1:
            embed = discord.Embed(title="じゃんけん", description="グー！私が負けました！", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None
        elif COM_val == 2:
            embed = discord.Embed(title="じゃんけん", description="パー！あいこですね！", color=0xf5c2d6)
            embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
            await ctx.channel.send("<@{}>".format(ctx.author.id), embed=embed)
            return None

    else:
        await ctx.send("<@{}> チョキ、グー、パーの中で一つを入力してください！".format(ctx.author.id))
        return None

@bot.command(name="join")
async def join(ctx):
    global chnl
    global k_koe
    global j_koe
    global voice

    guild = ctx.guild
    guild_id = ctx.guild.id
    try:
        channel = ctx.author.voice.channel
        voice_ = get(ctx.bot.voice_clients, guild=ctx.guild)

        if voice_ and voice_.is_connected():
            await voice_.move_to(channel)
            await ctx.send("BOT入場（移動） - **{0}**".format(channel))
            chnl[guild_id] = ctx.channel.id
            voice[guild_id] = ctx.guild.voice_client
        else:
            await channel.connect()
            await ctx.send("BOT入場 - **{0}**".format(channel))
            chnl[guild_id] = ctx.channel.id
            k_koe[guild_id] = k_de
            j_koe[guild_id] = j_de
            voice[guild_id] = ctx.guild.voice_client
    except:
        await ctx.send("ボイスチャンネルに入った状態でこのコマンドを入力してください！")
        return None

def removeAllFile(filePath):
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
        return 'Remove All File'
    else:
        return 'Directory Not Found'

@bot.command(name="dis")
async def dis(ctx):
    global voice

    guild_id = ctx.guild.id
    voice_client = ctx.message.guild.voice_client
    if not voice_client:
        await ctx.send("BOTがこのサーバーのボイスチャンネルに入ってません！")
        print(removeAllFile('[Location]\TTS'))
        return None

    await ctx.send("BOT DISCONNECT 完了")
    await voice_client.disconnect()
    del(voice[guild_id])
    print(removeAllFile('[Location]\TTS'))

@bot.command()
async def avatar(ctx, *, avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    embed = discord.Embed(title="", description="", color=0xf5c2d6)
    embed.set_image(url=userAvatarUrl)
    embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
    await ctx.channel.send(embed=embed)

@bot.command()
async def neko(ctx):
    embed = discord.Embed(title="", description="", color=0xf5c2d6)
    embed.set_image(url=nekos.cat())
    embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
    await ctx.channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return None

    global j_de
    global k_de
    global k_koe
    global j_koe
    global chnl
    global channel_t

    global voice

    channel = message.channel
    channel_id = message.channel.id
    guild_id = message.author.guild.id
    channel_t[guild_id] = message.channel

    guild = message.author.guild

    voice[guild_id] = message.guild.voice_client
    t = list(str(channel))

    if voice[guild_id]:
        if chnl[guild_id] == channel_id:
            txt = list(message.content)
            for i in range(len(txt)):
                if txt[i] == '\n':
                    txt[i] = ' '

            if txt[0] != '*' and txt[0] != '^' and txt[0] != '~':
                txt = ''.join(txt)

                m = re.search(r'https?', txt)

                if m == None:
                    pattern = "<@![0-9]*>"
                    if re.search(pattern, txt) != None:
                        num1, num2 = re.search(pattern, txt).span()

                        user_id = int(txt[num1+3:num2-1])
                        #user = await bot.fetch_user(user_id)
                        try:
                            txt = txt.replace(txt[num1:num2], guild.get_member(user_id).nick) 
                        except:
                            txt = txt.replace(txt[num1:num2], guild.get_member(user_id).name)
                    
                    emoji_pattern = ":\d+>"
                    if re.search(emoji_pattern, txt) != None:
                        txt = re.sub(emoji_pattern, '', txt)


                    encQuery = urllib.parse.quote(txt)
                    data = "query=" + encQuery
                    url = "https://openapi.naver.com/v1/papago/detectLangs"
                    request = urllib.request.Request(url)
                    request.add_header("X-Naver-Client-Id",v_client_id)
                    request.add_header("X-Naver-Client-Secret",v_client_secret)
                    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                    rescode = response.getcode()
                    if(rescode==200):
                        response_body = response.read()
                        lan_det = response_body.decode('utf-8')[13:15]
                    else:
                        print("Error Code:" + rescode)

                    if lan_det == 'ja':
                        input = texttospeech.SynthesisInput(text=txt)
                        voice_t = texttospeech.VoiceSelectionParams(
                            language_code='ja-JP',
                            name = 'ja-JP-Standard-{}'.format(j_koe[guild_id]),
                            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
                        audio_config = texttospeech.AudioConfig(
                            audio_encoding=texttospeech.AudioEncoding.MP3)
                        response = client.synthesize_speech(input=input, voice=voice_t, audio_config=audio_config)

                        N = random.randrange(0,99999999999)

                        with open('[Location]\TTS\{}.mp3'.format(N), 'wb') as out:
                            out.write(response.audio_content)

                        guild = message.author.guild
                        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
                        audio_source = discord.FFmpegPCMAudio('[Location]\TTS\{}.mp3'.format(N))

                        while voice_client.is_playing():
                            await asyncio.sleep(1)

                        if not voice_client.is_playing():
                            voice_client.play(audio_source, after=None)
                            await asyncio.sleep(0.5)

                    elif lan_det == 'ko':
                        input = texttospeech.SynthesisInput(text=txt)
                        voice_t = texttospeech.VoiceSelectionParams(
                            language_code='ko-KR',
                            name='ko-KR-Standard-{}'.format(k_koe[guild_id]),
                            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
                        audio_config = texttospeech.AudioConfig(
                            audio_encoding=texttospeech.AudioEncoding.MP3)
                        response = client.synthesize_speech(input=input, voice=voice_t, audio_config=audio_config)

                        N = random.randrange(0, 99999999999)

                        with open('[Location]\TTS\{}.mp3'.format(N), 'wb') as out:
                            out.write(response.audio_content)

                        guild = message.author.guild
                        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
                        audio_source = discord.FFmpegPCMAudio('[Location]\TTS\{}.mp3'.format(N))

                        while voice_client.is_playing():
                            await asyncio.sleep(1)

                        if not voice_client.is_playing():
                            voice_client.play(audio_source, after=None)
                            await asyncio.sleep(0.5)
                    
                    else:
                        input = texttospeech.SynthesisInput(text=txt)
                        voice_t = texttospeech.VoiceSelectionParams(
                            language_code='ko-KR',
                            name='ko-KR-Standard-{}'.format(k_koe[guild_id]),
                            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
                        audio_config = texttospeech.AudioConfig(
                            audio_encoding=texttospeech.AudioEncoding.MP3)
                        response = client.synthesize_speech(input=input, voice=voice_t, audio_config=audio_config)

                        N = random.randrange(0, 99999999999)

                        with open('[Location]\TTS\{}.mp3'.format(N), 'wb') as out:
                            out.write(response.audio_content)

                        guild = message.author.guild
                        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
                        audio_source = discord.FFmpegPCMAudio('[Location]\TTS\{}.mp3'.format(N))

                        while voice_client.is_playing():
                            await asyncio.sleep(1)

                        if not voice_client.is_playing():
                            voice_client.play(audio_source, after=None)
                            await asyncio.sleep(0.5)

    if t[0] == '_':
        txt = list(message.content)
        if txt[0] != '^':
            if message.author.bot:
                return None
            txt = str(message.content)

            encQuery = urllib.parse.quote(txt)
            data = "query=" + encQuery
            url = "https://openapi.naver.com/v1/papago/detectLangs"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",v_client_id)
            request.add_header("X-Naver-Client-Secret",v_client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                lan_det = response_body.decode('utf-8')[13:15]
            else:
                print("Error Code:" + rescode)

            if lan_det == 'ko':
                ID = message.author.id
                TR = await translate_ko_to_ja(txt, ID)
                await channel.send(TR)

            elif lan_det == 'ja':
                ID = message.author.id
                TR = await translate_ja_to_ko(txt, ID)
                await channel.send(TR)
            else:
                ID = message.author.id
                TR = await translate_etc_to_ko(txt, ID, lan_det)
                await channel.send(TR)

    await bot.process_commands(message)

@bot.command()
async def change_ko(ctx, message):
    global k_de
    global k_koe

    guild_id = ctx.guild.id

    try:
        if k_koe[guild_id] == message:
            await ctx.send("이미 {}로 설정되어있습니다!".format(k_koe[guild_id]))
            return None

        for tx in k_list:
            if message == tx:
                S = k_koe[guild_id] + ' -> ' + message
                await ctx.send(S)
                k_koe[guild_id] = message
                return None

        await ctx.send("목록 중 하나를 선택해주세요!")
    except:
        await ctx.send("^join 명령어 입력 후 이 명령어를 사용해주세요!")
    return None

@bot.command()
async def change_jp(ctx, message):
    global j_de
    global j_koe

    guild_id = ctx.guild.id

    try:
        if j_koe[guild_id] == message:
            await ctx.send("既に{}に設定されています！".format(j_koe[guild_id]))
            return None
        for tx in j_list:
            if message == tx:
                S = j_koe[guild_id] + ' -> ' + message
                await ctx.send(S)
                j_koe[guild_id] = message
                return None

        await ctx.send("リストの中で一つを選んでください！")
    except:
        await ctx.send("^joinコマンドを入力してからこのコマンドを使用してください！")
    return None

async def translate_ko_to_ja(message, ID):
    encText = urllib.parse.quote(message)
    data = "source=ko&target=ja&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", v_client_id)
    request.add_header("X-Naver-Client-Secret", v_client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        res = response_body.decode('utf-8')
        import json
        res = json.loads(res)
        print(res['message']['result']['translatedText'])
        text = '<@{}> **{}**'.format(ID, res['message']['result']['translatedText'])
        return text
    else:
        print("Error Code:" + rescode)

async def translate_ja_to_ko(message, ID):
    encText = urllib.parse.quote(message)
    data = "source=ja&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", v_client_id)
    request.add_header("X-Naver-Client-Secret", v_client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        res = response_body.decode('utf-8')
        import json
        res = json.loads(res)
        print(res['message']['result']['translatedText'])
        text = '<@{}> **{}**'.format(ID, res['message']['result']['translatedText'])
        return text
    else:
        print("Error Code:" + rescode)

async def translate_etc_to_ko(message, ID, lang):
    encText = urllib.parse.quote(message)
    data = f"source={lang}&target=ja&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", v_client_id)
    request.add_header("X-Naver-Client-Secret", v_client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        res = response_body.decode('utf-8')
        import json
        res = json.loads(res)
        print(res['message']['result']['translatedText'])
        text = '<@{}> **{}**'.format(ID, res['message']['result']['translatedText'])
        return text
    else:
        print("Error Code:" + rescode)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="KaniChaBot's Help Command", color=0xf5c2d6)
    embed.add_field(name="help_ko", value="한국어버전 카니챠봇의 설명서를 확인하실 수 있습니다!", inline=False)
    embed.add_field(name="help_jp", value="日本語バージョンカニ茶ボットの説明書を確認できます！", inline=False)
    embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
    embed.set_thumbnail(url="https://i.imgur.com/v7FHQp4.png")
    await ctx.channel.send(embed=embed)


@bot.command()
async def help_ko(ctx):
    embed = discord.Embed(title="설명서", description="카니챠봇의 모든 명령어를 확인하실 수 있습니다!", color=0xf5c2d6)
    embed.add_field(name="가위바위보", value="봇과 가위바위보를 할 수 있습니다!\nex)^가위바위보 보")
    embed.add_field(name="じゃんけん", value="일본어버전의 가위바위보 입니다!\nex)じゃんけん パー")
    embed.add_field(name="join", value="TTS기능의 봇을 보이스채팅방에 불러옵니다.", inline=False)
    embed.add_field(name="dis", value="TTS기능의 봇을 보이스채팅방에서 내보냅니다.", inline=False)
    embed.add_field(name="change_ko", value="한국어 TTS 음성을 바꿀 수 있습니다!\n'A': 여성 음색, 'B': 여성 음색, 'C': 남성 음색, 'D': 남성 음색\nex)^change_ko B")
    embed.add_field(name="change_jp", value="일본어 TTS 음성을 바꿀 수 있습니다!\n'A': 여성 음색, 'B': 여성 음색, 'C': 남성 음색, 'D': 남성 음색\nex)^change_jp A")
    embed.add_field(name="avatar", value="명령어 뒤에 [@닉네임]을 입력하시면 [@닉네임]의 프로필 사진 원본을 확인하실 수 있습니다!\nex)^avatar @カニ茶ボット", inline=False)
    embed.add_field(name="imgsrch", value="구글에서 351x351 이상의 랜덤 이미지를 검색해줍니다!\nex)^imgsrch 고양이", inline=False)
    embed.add_field(name="neko", value="random neko image!")
    embed.add_field(name="번역기능", value="이 것은 명령어가 아닌 상시 켜져있는 봇의 기능으로 '_'로 시작하는 게시판에 한국어 혹은 일본어를 입력하면 그 반대의 언어로 번역해줍니다!", inline=False)
    embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
    embed.set_thumbnail(url="https://i.imgur.com/v7FHQp4.png")
    await ctx.channel.send(embed=embed)

@bot.command()
async def help_jp(ctx):
    embed = discord.Embed(title="説明書", description="カニ茶ボットの使えるコマンドをここで確認できます！", color=0xf5c2d6)
    embed.add_field(name="가위바위보", value="韓国語バージョンのじゃんけんです！\nex)^가위바위보 보")
    embed.add_field(name="じゃんけん", value="BOTとじゃんけんで遊べます！\nex)^じゃんけん パー")
    embed.add_field(name="join", value="TTSボットをボイスチャンネルに呼び出します。", inline=False)
    embed.add_field(name="dis", value="TTSボットをボイスチャンネルから切断します。", inline=False)
    embed.add_field(name="change_ko", value="韓国語TTSの音声を変えることができます！\n'A': 女性音色, 'B': 女性音色, 'C': 男性音色, 'D': 男性音色\nex)^change_ko B")
    embed.add_field(name="change_jp", value="日本語TTSの音声を変えることができます！\n'A': 女性音色, 'B': 女性音色, 'C': 男性音色, 'D': 男性音色\nex)^change_jp A")
    embed.add_field(name="avatar", value="コマンドの後ろに[@ニックネーム]を入力したら[@ニックネーム]のオリジナルプロフィール画像を確認できます！\nex)^avatar @カニ茶ボット", inline=False)
    embed.add_field(name="imgsrch", value="Googleから351x351以上のランダムイメージを検索してくれます！\nex)^imgsrch 猫", inline=False)
    embed.add_field(name="neko", value="random neko image!")
    embed.add_field(name="翻訳機能", value="これはコマンドではなく常時ONされてるBOTの機能で'_'で始まる掲示板に韓国語または日本語を入力したらその逆の言語で翻訳してくれます！", inline=False)
    embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
    embed.set_thumbnail(url="https://i.imgur.com/v7FHQp4.png")
    await ctx.channel.send(embed=embed)

bot.run('[Discord Bot Token]')