# Discord.py Rewrite

# API List
# Naver Papago(Free), Naver Language Detection(Free),
# Google Text-to-Speech(Free)

# Hosting
# vultr.com / 1024MB HIGH FREQUENCY

# BOT 招待リンク | BOT 초대 링크
# 1 https://discord.com/oauth2/authorize?client_id=783369247060656169&permissions=8&scope=bot
# 2 https://discord.com/oauth2/authorize?client_id=783237963609276416&permissions=8&scope=bot
# 3 https://discord.com/oauth2/authorize?client_id=847840100225646662&permissions=8&scope=bot

import discord
from discord.ext import commands

import asyncio
import re
import os
import random
import urllib.request

from google.cloud import texttospeech

intents = discord.Intents().default()
intents.members = True

bot = commands.Bot(command_prefix='^', intents = intents)
bot.remove_command("help")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="[Google API File PATH]"

client = texttospeech.TextToSpeechClient()

v_client_id = "[Naver Client id]"
v_client_secret = "[Naver Client Secret]"

chnl = {}

voice = {}

# Print guild list and set bot's status
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

# Join author's voice channel
@bot.command(name="join")
async def join(ctx):
    global chnl
    global voice

    guild = ctx.guild
    guild_id = ctx.guild.id
    try:
        channel = ctx.author.voice.channel
        voice_ = bot.get(ctx.bot.voice_clients, guild=ctx.guild)

        if voice_ and voice_.is_connected():
            await voice_.move_to(channel)
            await ctx.send("BOT入場（移動） - **{0}**".format(channel))
            chnl[guild_id] = ctx.channel.id
            voice[guild_id] = ctx.guild.voice_client
        else:
            await channel.connect()
            await ctx.send("BOT入場 - **{0}**".format(channel))
            chnl[guild_id] = ctx.channel.id
            voice[guild_id] = ctx.guild.voice_client
    except Exception as e:
        print('Error!', e)
        await ctx.send("ボイスチャンネルに入った状態でこのコマンドを入力してください！")
        return None

# Delete all mp3 files in the TTS folder when the command 'dis' is entered
def removeAllFile(filePath):
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
        return 'Remove All File'
    else:
        return 'Directory Not Found'

# Leave voice channel
@bot.command(name="dis")
async def dis(ctx):
    global voice

    guild_id = ctx.guild.id
    voice_client = ctx.message.guild.voice_client
    if not voice_client:
        await ctx.send("BOTがこのサーバーのボイスチャンネルに入ってません！")
        print(removeAllFile('[PATH]\TTS'))
        return None

    await ctx.send("BOT DISCONNECT 完了")
    await voice_client.disconnect()
    del(voice[guild_id])
    print(removeAllFile('[PATH]\TTS'))

# Show profile picture of a user who has been mentioned
@bot.command()
async def avatar(ctx, *, avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    embed = discord.Embed(title="", description="", color=0xf5c2d6)
    embed.set_image(url=userAvatarUrl)
    embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
    await ctx.channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return None

    global chnl
    global voice

    channel = message.channel
    channel_id = message.channel.id
    guild_id = message.author.guild.id
    guild = message.author.guild

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
                            name = 'ja-JP-Standard-B',
                            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
                        audio_config = texttospeech.AudioConfig(
                            audio_encoding=texttospeech.AudioEncoding.MP3)
                        response = client.synthesize_speech(input=input, voice=voice_t, audio_config=audio_config)

                        N = random.randrange(0,99999999999)

                        with open('[PATH]\TTS\{}.mp3'.format(N), 'wb') as out:
                            out.write(response.audio_content)

                        guild = message.author.guild
                        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
                        audio_source = discord.FFmpegPCMAudio('[PATH]\TTS\{}.mp3'.format(N))

                        while voice_client.is_playing():
                            await asyncio.sleep(1)

                        if not voice_client.is_playing():
                            voice_client.play(audio_source, after=None)
                            await asyncio.sleep(0.5)

                    elif lan_det == 'ko':
                        input = texttospeech.SynthesisInput(text=txt)
                        voice_t = texttospeech.VoiceSelectionParams(
                            language_code='ko-KR',
                            name='ko-KR-Standard-A',
                            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
                        audio_config = texttospeech.AudioConfig(
                            audio_encoding=texttospeech.AudioEncoding.MP3)
                        response = client.synthesize_speech(input=input, voice=voice_t, audio_config=audio_config)

                        N = random.randrange(0, 99999999999)

                        with open('[PATH]\TTS\{}.mp3'.format(N), 'wb') as out:
                            out.write(response.audio_content)

                        guild = message.author.guild
                        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
                        audio_source = discord.FFmpegPCMAudio('[PATH]\TTS\{}.mp3'.format(N))

                        while voice_client.is_playing():
                            await asyncio.sleep(1)

                        if not voice_client.is_playing():
                            voice_client.play(audio_source, after=None)
                            await asyncio.sleep(0.5)
                    
                    else:
                        input = texttospeech.SynthesisInput(text=txt)
                        voice_t = texttospeech.VoiceSelectionParams(
                            language_code='ja-JP',
                            name='ja-JP-Standard-B',
                            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
                        audio_config = texttospeech.AudioConfig(
                            audio_encoding=texttospeech.AudioEncoding.MP3)
                        response = client.synthesize_speech(input=input, voice=voice_t, audio_config=audio_config)

                        N = random.randrange(0, 99999999999)

                        with open('[PATH]\TTS\{}.mp3'.format(N), 'wb') as out:
                            out.write(response.audio_content)

                        guild = message.author.guild
                        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
                        audio_source = discord.FFmpegPCMAudio('[PATH]\TTS\{}.mp3'.format(N))

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

# Translate Korean to Japanese
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

# Translate Japanese to Korean
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

# Translate Others to Korean
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
    embed.add_field(name="join", value="TTS기능의 봇을 보이스채팅방에 불러옵니다.", inline=False)
    embed.add_field(name="dis", value="TTS기능의 봇을 보이스채팅방에서 내보냅니다.", inline=False)
    embed.add_field(name="avatar", value="명령어 뒤에 [@닉네임]을 입력하시면 [@닉네임]의 프로필 사진 원본을 확인하실 수 있습니다!\nex)^avatar @カニ茶ボット", inline=False)
    embed.add_field(name="번역기능", value="이 것은 명령어가 아닌 상시 켜져있는 봇의 기능으로 '_'로 시작하는 게시판에 한국어 혹은 일본어를 입력하면 그 반대의 언어로 번역해줍니다!", inline=False)
    embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
    embed.set_thumbnail(url="https://i.imgur.com/v7FHQp4.png")
    await ctx.channel.send(embed=embed)

@bot.command()
async def help_jp(ctx):
    embed = discord.Embed(title="説明書", description="カニ茶ボットの使えるコマンドをここで確認できます！", color=0xf5c2d6)
    embed.add_field(name="join", value="TTSボットをボイスチャンネルに呼び出します。", inline=False)
    embed.add_field(name="dis", value="TTSボットをボイスチャンネルから切断します。", inline=False)
    embed.add_field(name="avatar", value="コマンドの後ろに[@ニックネーム]を入力したら[@ニックネーム]のオリジナルプロフィール画像を確認できます！\nex)^avatar @カニ茶ボット", inline=False)
    embed.add_field(name="翻訳機能", value="これはコマンドではなく常時ONされてるBOTの機能で'_'で始まる掲示板に韓国語または日本語を入力したらその逆の言語で翻訳してくれます！", inline=False)
    embed.set_footer(text="KaniChaBot", icon_url="https://i.imgur.com/v7FHQp4.png")
    embed.set_thumbnail(url="https://i.imgur.com/v7FHQp4.png")
    await ctx.channel.send(embed=embed)

bot.run('[Discord Bot Token]')
