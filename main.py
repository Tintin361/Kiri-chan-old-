from __future__ import unicode_literals
from ast import alias
from unicodedata import name
import discord
from discord import voice_client
from discord.embeds import Embed
from discord.ext import commands
from discord.player import FFmpegPCMAudio
from discord.voice_client import VoiceClient
import list_of_things, not_important
import reddit as red
from termcolor import colored
from datetime import datetime as dt
import pytz
import random
import yt_dlp as youtube_dl
import twitter as tw
import os.path, platform
import validators

DISCORD_TOKEN = not_important.bot_token
safebooru_password = not_important.reddit_password

client = discord.Client
bot = commands.Bot(command_prefix="-", help_command=None)

ver = "1.2.3"
user_id = 443113150599004161
listmod = list_of_things.rlist()
online_message = "des tonnes d'octets"
voice = None
timezone = pytz.timezone('Europe/Paris')
last_message = None

def get_time():
    now = dt.now(timezone)
    time = now.strftime("%d/%m/%Y - %H:%M:%S")

    return time

# Write content in a .txt file
def write_in_txt(content, file):
    with open(file, "w") as f:
        f.write(str(content))

# Youtube-downloader file's options
save_path = "/var/www/html/youtube_audios/"
video_save_path = "/var/www/html/youtube_audios/"
ydl_mp3 = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl':save_path + '%(id)s.%(ext)s',
}
ydl_ogg = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'vorbis',
        'preferredquality': '192',
    }],
    'outtmpl':save_path + '%(id)s.%(ext)s',
}
ydl_mkv = {'format' : 'bestvideo+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
    'merge-output-format' : 'mkv',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mkv'
    }],
    'outtmpl':video_save_path + '%(id)s.%(ext)s',
}

def get_video_id(url, opts):
    with youtube_dl.YoutubeDL(opts) as ydl:
        infos = ydl.extract_info(url, download=False)
        video_id = infos.get("id", None)
        video_title = infos.get("title", None)
        return video_id, video_title

def get_video_data(content, format, is_query):
    with youtube_dl.YoutubeDL(format) as ydl:
        if is_query:
            infos = ydl.extract_info(f"ytsearch:{content}", download=False)['entries'][0]
            id = infos.get("id", None)
            title = infos.get("title", None)
            url = infos.get("video_url", None)
            return id, title
        else:
            infos = ydl.extract_info(content, download=False)
            id = infos.get("id", None)
            title = infos.get("title", None)
            return id, title
        

def youtube_audio_downloader(url, format):
    if format == "mp3":
        with youtube_dl.YoutubeDL(ydl_mp3) as ydl:
            ydl.download([url])
    elif format == "ogg":
        with youtube_dl.YoutubeDL(ydl_ogg) as ydl:
            ydl.download([url])
    elif format == "mkv":
        with youtube_dl.YoutubeDL(ydl_mkv) as ydl:
            ydl.download([url])

@bot.event
async def on_ready():
    print('Connecté en tant que: ' + colored('{0.user}'.format(bot), "cyan") + " - Kiri-chan prête !")
    print(f"Version Python: {platform.python_version()} - Version Discord.py: {discord.__version__ } - Version du bot: {ver}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=online_message))

@bot.listen()
async def on_message(msg):
    username = await bot.fetch_user(msg.author.id)
    author = ""
    # Write messages in history.txt
    if msg.author.id == 789984188224110632:
        author = "Kiri-chan"
        color = "cyan"
    elif msg.author.id == 443113150599004161:
        author = "Tintin"
        color = "yellow"
    elif msg.author.id == 370169515515838465:
        author = "Celian.msi"
        color = "green"
    else:
        author = username
        color = "blue"

    if str(msg.content) == "":
        content = "[image]" 
    else:
        content = str(msg.content)

    if msg.author == bot.user:
        return

    global listmod

    if content.startswith("-"):
        print(f"{colored(username, color)}: {content}")

    try:
        if msg.author.id != 443113150599004161:
            if msg.channel.id == msg.author.dm_channel.id:
                user = await bot.fetch_user(443113150599004161)
                await user.send(str(author) + ":\n" + msg.content)
    except:
        pass

    if msg.channel.id == 935514239035142164 and not msg.content.startswith("-"):
        await msg.delete()

    hist = open("history.txt", "a")
    time = get_time()

    hist.write(time + " - " + str(username) + ": " + content + "\n")

    if bot.user.mentioned_in(msg) and msg.mention_everyone is False:
        await msg.channel.send("Utilise -help pour voir la liste des commandes.")

    write_in_txt(msg.id, "last_message.txt")


# Ping command
@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send(f"Latence: {bot.latency * 1000} ms.")


# Command for join a channel
@bot.command(name='join', aliases=['joinVC'])
async def join(ctx):
    if ctx.author.id in listmod:
        await ctx.message.delete()
        voice_player = await ctx.message.author.voice.channel.connect()


# Random one
@bot.command()
async def poyo(ctx):
    await ctx.message.delete()
    await ctx.send("POYO !!!")


# Play cheh sound in a voice channel
@bot.command()
async def cheh(ctx):
    await ctx.message.delete()
    channel = ctx.message.author.voice.channel
    global voice
    voice = await channel.connect()
    if voice.is_playing():
        voice.stop()
    voice.play(discord.FFmpegPCMAudio(f"{save_path}cheh.mp3"))
    await ctx.voice_client.disconnect()


# Reddit commands
@bot.command()
async def last(ctx, arg):
    await ctx.message.delete()
    try:
        red.last_post(arg)
    except:
        await ctx.send("Désolée, je n'ai pas trouvé le subreddit... :mag_right:")
        return

    result = red.last_post(arg)
    title = result[0]
    url = result[1]
    sub_title = result[2]
    id = result[3]
    nsfw = result[4]
    author = result[5]

    if nsfw == "True":
        if not ctx.channel.is_nsfw():
            await ctx.send("<:nsfw:719673214644781056> Ce post contient du contenu NSFW, pour voir ce contenu, utilise la commande dans un salon NSFW.")
            return
    write_in_txt(str(id), "reddit_data.txt")
    await ctx.send(f"**Voici le dernier post sur r/{sub_title} par u/{author}:**\n{title}\n\n{url}\n(ID: {id})")

@bot.command()
async def hot(ctx, arg):
    await ctx.message.delete()
    try:
        red.last_post(arg)
    except:
        await ctx.send("Désolée, je n'ai pas trouvé le subreddit... :mag_right:")
        return

    result = red.hot_post(arg)
    title = result[0]
    url = result[1]
    sub_title = result[2]
    id = result[3]
    nsfw = result[4]
    author = result[5]

    if nsfw == "True":
        if not ctx.channel.is_nsfw():
            await ctx.send("<:nsfw:719673214644781056> Ce post contient du contenu NSFW, pour voir ce contenu, utilise la commande dans un salon NSFW.")
            return
    write_in_txt(str(id), "reddit_data.txt")
    await ctx.send(f"**Voici le dernier post sur r/{sub_title} par u/{author}:**\n{title}\n\n{url}\n(ID: {id})")

@bot.command(name="fakehistory", aliases=['FakeHistoryPorn', 'FakeHistory', 'fakeHistory', 'Fakehistory'])
async def fakehistory(ctx):
    await ctx.message.delete()

    result = red.get("fakehistoryporn", 50)
    title = result[0]
    url = result[1]
    id = result[2]
    nsfw = result[3]
    author = result[4]

    if nsfw == "True":
        if not ctx.channel.is_nsfw():
            await ctx.send("<:nsfw:719673214644781056> Ce post contient du contenu NSFW, pour voir ce contenu, utilise la commande dans un salon NSFW.")
            return
    write_in_txt(str(id), "reddit_data.txt")
    await ctx.send(f"**Voici le dernier post sur r/FakeHistory par u/{author}:**\n{title}\n\n{url}\n(ID: {id})")

@bot.command()
async def wallpaper(ctx):
    await ctx.message.delete()

    result = red.get("wallpaper", 30)
    title = result[0]
    url = result[1]
    id = result[2]
    author = result[4]

    write_in_txt(str(id), "reddit_data.txt")
    await ctx.send(f"**Voici le dernier post sur r/Wallpaper par u/{author}:**\n{title}\n\n{url}\n(ID: {id})")

@bot.command()
async def honkai(ctx):
    await ctx.message.delete()

    result = red.get("houkai3rd", 30)
    title = result[0]
    url = result[1]
    id = result[2]
    nsfw = result[3]
    author = result[4]

    if nsfw == "True":
        if not ctx.channel.is_nsfw():
            await ctx.send("<:nsfw:719673214644781056> Ce post contient du contenu NSFW, pour voir ce contenu, utilise la commande dans un salon NSFW.")
            return
    write_in_txt(str(id), "reddit_data.txt")
    await ctx.send(f"**Voici le dernier post sur r/Houkai3rd par u/{author}:**\n{title}\n\n{url}\n(ID: {id})")

@bot.command()
async def crappy(ctx):
    await ctx.message.delete()

    result = red.get("crappydesign", 30)
    title = result[0]
    url = result[1]
    id = result[2]
    author = result[4]

    write_in_txt(str(id), "reddit_data.txt")
    await ctx.send(f"**Voici le dernier post sur r/CrappyDesign par u/{author}:**\n{title}\n\n{url}\n(ID: {id})")

@bot.command(name='upvote', aliases=['up'])
async def upvote(ctx):
    await ctx.message.delete()
    id = "None"
    with open("reddit_data.txt", "r") as f:
        id = f.read()
    if id == "None":
        await ctx.send("Désolée, je n'ai pas d'ID dans mes fichier...")
        return
    result = red.upvote(id)
    if result == "False":
        await ctx.send("Erreur: Je n'ai pas pu upvoter le post...")
    elif result == "Null":
        await ctx.send("Le post a bien été upvoté mais je ne peux pas récupérer le score...")
    else:
        score = int(result)
        await ctx.send(f"Le post a bien été upvoté ! (Score: {score})")

@bot.command()
async def score(ctx, id):
    await ctx.message.delete()
    score = red.score(id)
    await ctx.send(f"Le score du post est de {score}")


# Time function
@bot.command(name="datetime")
async def datetime(ctx):
    await ctx.message.delete()
    time = get_time()
    await ctx.send(f"On est le {time}")


# Random number function
@bot.command()
async def randomNum(ctx, arg1: int, arg2: int):
    await ctx.message.delete()
    result = random.randint(arg1, arg2)
    await ctx.send(f"J'ai choisis le nombre: {result}")


# Change Kiri-chan's nickname in the server
@bot.command()
async def pseudo(ctx, *arg):
    await ctx.message.delete()
    name = ' '.join(arg)
    await ctx.guild.get_member(bot.user.id).edit(nick=name)
    await ctx.send(f'Mon nouveau pseudo c\'est: **{name}**')

# Change user nickname
@bot.command()
async def nick(ctx, *arg):
    await ctx.message.delete()
    name = ' '.join(arg)
    member = await ctx.guild.fetch_member(ctx.message.author.id)
    try:
        await member.edit(nick=name)
    except discord.Forbidden:
        await ctx.send("Désolée, je ne peux pas changer ton pseudo, je n'ai pas les permissions... :confused:")
        return
    await ctx.channel.send(f"{ctx.author.mention} J\'ai changé ton pseudo, c\'est maintenant: **{name}** !")


# Download and convert a video and return an URL
@bot.command(name="dlYoutube", aliases=['dlyt', 'ytdl'])
async def dlYoutube(ctx, url, format="mp3"):
    await ctx.message.delete()

    if format == "mkv":
        video_id, video_title = get_video_id(url, ydl_mkv)
        file_exist = os.path.exists(f"/var/www/html/youtube_videos/{video_id}.{format}")
    else:
        video_id, video_title = get_video_id(url, ydl_mp3)
        file_exist = os.path.exists(f"/var/www/html/youtube_audios/{video_id}.{format}")
    
    if file_exist == False:
        message = await ctx.send("Le téléchargement est en cours, je ne serais plus disponible...")
        youtube_audio_downloader(url, format)
        await message.delete()

    if format == "mkv":
        await ctx.send(f"Voici l'URL du fichier: http://91.174.152.111:35080/youtube_videos/{video_id}.{format}")
    else:
        await ctx.send(f"Voici l'URL du fichier: http://91.174.152.111:35080/youtube_audios/{video_id}.{format}")

# Same as dlYoutube but play it in voice channel
@bot.command(name="play")
async def play(ctx, *content):
    await ctx.message.delete()
    query = ' '.join(content)

    search_msg = await ctx.send("<a:search:944484192018903060> Recherche de la vidéo sur YouTube en cours...")

    check_url = validators.url(query)
    if check_url == True:
        id, title = get_video_data(query, ydl_mp3, False)
        url = query
    else:
        id, title = get_video_data(query, ydl_mp3, True)
        url = f"https://www.youtube.com/watch?v={id}"
        
    thumbnail = f"(https://i.ytimg.com/vi/{id}/maxresdefault.jpg)"
    await search_msg.delete()
    file_exist = os.path.exists(f"{save_path}{id}.mp3")
    if file_exist == False:
        message = await ctx.send(f"Téléchargement et conversion de la vidéo:\n**{title}**\nJe ne suis pas encore multi-tâche donc je ne serais plus disponible.\n{thumbnail}")
        youtube_audio_downloader(url, "mp3")
        await message.delete()

    channel = ctx.message.author.voice.channel
    global voice
    try:
        voice = await channel.connect()
    except:
        pass
    if voice.is_playing():
        voice.stop()
    voice.play(discord.FFmpegPCMAudio(f"{save_path}{id}.mp3"))
    await ctx.send(f"Lecture de la vidéo:\n**{title}**\n{thumbnail}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=title))

# Stop the music
@bot.command(name='stop', aliases=['s'])
async def stop(ctx):
    await ctx.message.delete()
    global voice
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.send("Aucune musique n'est jouée actuellement")

# Play dream's speedrunning music in a voice channel
@bot.command()
async def dream(ctx):
    await ctx.message.delete()

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="la musique de Dream."))
    channel = ctx.message.author.voice.channel
    global voice
    voice = await channel.connect()
    if voice.is_playing():
        voice.stop()
    voice.play(discord.FFmpegPCMAudio(f"{save_path}dream.mp3"))

# Play Segs video
@bot.command()
async def segs(ctx):
    await ctx.message.delete()
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="SEEEEEEEGGGGSSS !!!!"))
    channel = ctx.message.author.voice.channel
    global voiceS
    voice = await channel.connect()
    if voice.is_playing():
        voice.stop()
    voice.play(discord.FFmpegPCMAudio(f"{save_path}segs.mp3"))

# Pause function
@bot.command(name='pause', aliases=['p'])
async def pause(ctx):
    await ctx.message.delete()
    try:
        await ctx.voice_client.pause()
    except:
        pass

# Resume the music
@bot.command()
async def resume(ctx):
    await ctx.message.delete()
    try:
        await ctx.voice_client.resume()
    except:
        pass

# Kiri-chan quit the voice channel
@bot.command(name='disconnect', aliases=['leave', 'dis'])
async def disconnect(ctx):
    await ctx.message.delete()
    try:
        await ctx.voice_client.disconnect()
    except:
        await ctx.send("Je ne suis connectée dans aucun salon vocal.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=online_message))

# Twitter's functions | Just tweet
@bot.command()
async def tweet(ctx, *msg):
    if ctx.author.id in listmod:
        message = ' '.join(str(i) for i in msg)
        await ctx.message.delete()
        tw.tweet(message)

# Get the first three tweet from @kirlia-chan timeline
@bot.command(name='timeline', aliases=['tl'])
async def timeline(ctx):
    if ctx.author.id in listmod:
        timeline = tw.get_timeline()
        for user, content in timeline.items():
            await ctx.send(f"{user}:\n{content}")


# Pybooru function | Safebooru
@bot.command(name='safebooru')
async def safe_search(ctx, search="default"):
    #result = booru.search_safebooru(search)
    #await ctx.send(result)
    pass


# Delete Messages Function
@bot.command(name="deleteMessage", aliases=['dlt', 'deletemessage', 'delete'])
async def delete(ctx, id):
    if ctx.author.id not in listmod:
        ctx.channel.send("Tu n'a pas les permissions pour cette commande !")
        return
    await ctx.message.delete()
    if id == None:
        with open ("last_message.txt", "r") as file:
            id = file.read()
    
    channel = bot.get_channel(ctx.channel.id)
    message = await channel.fetch_message(int(id))
    await message.delete()


# Imgflip functions - Unfinished
# @bot.command(name="")

# Upscale images functions - Unfinished
# @bot.command(name="upscale")
# async def upscale_image(ctx, x, y):
    # image = ctx.message.attachments[0]


# Help functions
@bot.command()
async def help(ctx):
    await ctx.message.delete()
    embedMsg = discord.Embed(title="Liste des commandes", description="Liste de toutes les catégories", color=0xffffff)
    embedMsg.add_field(name="<:reddit:794069835138596886> Reddit", value="-helpReddit", inline=False)
    embedMsg.add_field(name="<:youtube:316620060221374466> Youtube", value="-helpYoutube", inline=False)
    embedMsg.add_field(name=":robot: Features", value="-helpFeatures", inline=False)
    embedMsg.add_field(name=":screwdriver: Outils", value="-helpTools", inline=False)
    embedMsg.add_field(name="<:Modo:945135154131791912> Administratif", value="-helpAdmin", inline=False)

    await ctx.channel.send(embed=embedMsg)

@bot.command()
async def helpReddit(ctx):
    await ctx.message.delete()
    
    embedMsg = discord.Embed(title="<:reddit:794069835138596886> Reddit", description="Liste des commandes pour Reddit", color=0xff4300)
    embedMsg.add_field(name="-last [nom du subreddit]", value="Obtiens le dernier post d'un subreddit")
    embedMsg.add_field(name="-hot [nom du subreddit]", value="Obtiens un post populaire au hasard d'un subreddit")
    embedMsg.add_field(name="-fakehistory", value="Retourne un post du subreddit r/FakeHistoryPorn")
    embedMsg.add_field(name="-wallpaper", value="Retourne un post du subreddit r/Wallpaper")
    embedMsg.add_field(name="-honkai", value="Affiche un post du subreddit r/Houkai3rd")
    embedMsg.add_field(name="-crappy", value="Affiche un post du subreddit r/CrappyDesign")
    embedMsg.add_field(name="-upvote", value="Upvote le dernier post que j'affiche")
    embedMsg.add_field(name="-score [post]", value="Affiche le score du post")

    await ctx.channel.send(embed=embedMsg)

@bot.command()
async def helpYoutube(ctx):
    await ctx.message.delete()

    embedMsg = discord.Embed(title="<:youtube:316620060221374466> Youtube", description="Liste des commandes pour Youtube", color=0xFF0000)
    embedMsg.add_field(name="-ytdl [url] [format]", value="Télécharge une vidéo Youtube (formats disponibles: MP3, OOG, MKV)")
    embedMsg.add_field(name="-play [recherche ou url]", value="Joue une musique depuis Youtube dans un salon vocal")
    embedMsg.add_field(name="-pause", value="Met en pause la musique")
    embedMsg.add_field(name="-stop", value="Arrête la musique en cours")
    embedMsg.add_field(name="-resume", value="Reprends la musique là où tu l'avais arrêtée")
    embedMsg.add_field(name="-cheh", value="Quand le karma est contre toi...")
    embedMsg.add_field(name="-dream", value="Joue la musique de Dream dans un salon vocal")
    embedMsg.add_field(name="-segs", value="SEEEEEGGGGGGSSS !")
    embedMsg.add_field(name="-disconnect", value="Je quitte le salon vocal")

    await ctx.channel.send(embed=embedMsg)

@bot.command()
async def helpFeatures(ctx):
    await ctx.message.delete()

    embedMsg = discord.Embed(title=":robot: Features", description="Liste des commandes pour les features", color=0xed8a09)
    embedMsg.add_field(name="-poyo", value="POYO !")
    embedMsg.add_field(name="-pseudo [pseudonyme]", value="Change mon pseudo")
    embedMsg.add_field(name="-nick [pseudonyme]", value="Change ton pseudo si j'ai les per")
    embedMsg.add_field(name="-datetime", value="Je te donne l'heure")
    embedMsg.add_field(name="-randomNum [valeur 1] [valeur 2]", value="Je te donne un nombre aléatoire entre deux valeurs")

    await ctx.channel.send(embed=embedMsg)

@bot.command(name="helpOutils", aliases=['helpTools'])
async def helpOutils(ctx):
    await ctx.message.delete()

    embedMsg = discord.Embed(title=":screwdriver: Outils", description="Liste des commandes pour les outils", color=0x6d6d6d)
    embedMsg.add_field(name="-ping", value="Affiche la latence")
    embedMsg.add_field(name="-info", value="Obtiens des infos sur moi")
    embedMsg.add_field(name="-version", value="Obtiens le numéro de version")
    embedMsg.add_field(name="-github", value="Lien vers le repo sur GitHub.")

    await ctx.channel.send(embed=embedMsg)

@bot.command()
async def helpAdmin(ctx):
    await ctx.message.delete()

    embedMsg = discord.Embed(title="<:Modo:945135154131791912> Administratif", description="Liste des commandes uniquement pour les modérateurs", color=0xff00fa)
    embedMsg.add_field(name="-mpSet [ID utilisateur]", value="Permet de définir à qui j'envoie le Message Privé")
    embedMsg.add_field(name="-mp [contenu du message]", value="J'envoie le contenu de ton message")
    embedMsg.add_field(name="-join", value="Je rejoins le salon vocal dans lequel tu est connecté")
    embedMsg.add_field(name="-online [type] [message]", value="Je suis connectée")
    embedMsg.add_field(name="-idle [type] [message]", value="Je deviens inactive")
    embedMsg.add_field(name="-dnd [type] [message]", value="Ne me dérange pas")
    embedMsg.add_field(name="-invisible", value="Mais t'es pas là, mais t'es où ?")
    embedMsg.add_field(name="-shutdown", value="Arrêt du bot")

    await ctx.channel.send(embed=embedMsg)


# Shutdown the bot
@bot.command(name="shutdown", aliases=['sd'])
async def shutdown(ctx):
    await ctx.message.delete()
    if ctx.message.author.id in listmod:
        try:
            await ctx.voice_client.disconnect()
        except:
            pass
        await bot.logout()


@bot.command(name="informations", aliases=['info'])
async def informations(ctx):
    await ctx.channel.send('Je suis une bot encore en développement créée par Tintin.exe#6912 !')
    await ctx.message.delete()

@bot.command(name="version", aliases=['ver'])
async def version(ctx):
    global ver
    await ctx.message.delete()
    await ctx.send(f"Je suis en version {ver} !")


@bot.command(name="online")
async def online(ctx, activity="watch", message=online_message):
    await ctx.message.delete()
    if ctx.message.author.id not in listmod:
        await ctx.send("Tu n'a pas l'autorisation de changer mon statut")
        return
    
    activity = activity.lower()
    if activity == "watch" or activity == "watching":
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=message))
    elif activity == "listen":
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=message))
    elif activity == "game":
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=message))

@bot.command(name="idle")
async def idle(ctx, activity="watch", message="Splatoon 2 ou à Pokémon"):
    await ctx.message.delete()
    if ctx.message.author.id not in listmod:
        await ctx.send("Tu n'a pas l'autorisation de changer mon statut")
        return
    
    activity = activity.lower()
    if activity == "watch" or activity == "watching":
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=message))
    elif activity == "listen":
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name=message))
    elif activity == "game":
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=message))

@bot.command(name='dnd', aliases=['doNotDisturb', 'donotDisturb', 'donotdisturb'])
async def dnd(ctx, activity="watch", message="un anime (c\'est sympa Assassination Classroom !)"):
    await ctx.message.delete()
    if ctx.message.author.id not in listmod:
        await ctx.send("Tu n'a pas l'autorisation de changer mon statut")
        return
    
    activity = activity.lower()
    if activity == "watch" or activity == "watching":
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=message))
    elif activity == "listen":
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name=message))
    elif activity == "game":
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name=message))

@bot.command()
async def invisible(ctx):
    await ctx.message.delete()
    if ctx.author.id not in listmod:
        await ctx.send("Tu n'a pas l'autorisation de changer mon statut")
        return
    
    await bot.change_presence(status=discord.Status.invisible)


# Send a MP to a user with ID int
@bot.command()
async def mp(ctx, *arg):
    await ctx.message.delete()
    if ctx.message.author.id in listmod:
        content = ' '.join(arg)
        global user_id
        user = await bot.fetch_user(user_id)
        try:
            await user.send(content)
        except:
            await ctx.send("Désolée, impossible d'envoyer le MP.")
    else:
        await ctx.message.send("Tu n'a pas le droit d'envoyer un MP...")

# Set ID for mp command
@bot.command()
async def mpSet(ctx, arg):
    await ctx.message.delete()
    if ctx.message.author.id in listmod:
        global user_id
        user_id = int(arg)
    else:
        await ctx.message.send("Tu n'a pas le droit d'envoyer un MP...")


# Commands for Minecraft Server
@bot.command(name="getRole", aliases=['getrole', 'gr'])
async def getRole(ctx, role_name):
    await ctx.message.delete()
    list_of_non_roles = ["Modoux", "Kirlia-chan", "Bots"]

    guild = ctx.guild
    member = ctx.message.author
    if guild.id != 682267012709613580:
        await member.send("Cette commande n'est pas disponible pour ce serveur.")
        return
    elif role_name.capitalize() in list_of_non_roles:
        await member.send("Tu ne peux pas obtenir ce rôle.")
        return
    
    role = discord.utils.get(guild.roles, name = role_name.capitalize())
    await member.add_roles(role)

# Command to remove a role from a user
@bot.command(name="removeRole", aliases=['removerole', 'rr', 'rmrole'])
async def removeRole(ctx, role_name):
    await ctx.message.delete()
    guild = ctx.guild
    member = ctx.message.author
    if guild.id != 682267012709613580:
        await member.send("Cette commande n'est pas disponible pour ce serveur.")
        return
    
    roles = discord.utils.find(lambda r: r.name == 'Member', ctx.message.guild.roles)
    if roles not in member.roles:
        await member.send(f"Tu ne possède pas le rôle {role_name.capitalize()}.")
        return
    role_get = discord.utils.get(guild.roles, name = role_name.capitalize())
    await member.remove_roles(role_get)


# Role creator
@bot.command(name="createRole", aliases=['cr', 'createrole'])
async def createRole(ctx, *roleName):
    await ctx.message.delete()
    if ctx.message.author.id in listmod:
        content = ' '.join(roleName)
        await ctx.guild.create_role(name=content)


# Github repo
@bot.command(name="github", aliases=['GitHub', 'Github', 'gitHub'])
async def gif(ctx):
    await ctx.message.delete()
    await ctx.send("Lien vers le repo GitHub:\nhttps://github.com/Tintin361/Kiri-chan")


# Command error event
@bot.event
async def on_command_error(ctx, error):
    msg = ctx.message.content
    if ctx.message.author.id in listmod:
        if str(error) == "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'channel'":
            await ctx.send("Tu dois être dans un salon vocal pour que je puisse me connecter.")
        elif str(error) == "arg is a required argument that is missing.":
            await ctx.send("Tu dois ajouter un argument pour cette commande.")
        elif str(error) == "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'id'":
            await ctx.message.author.send("Ce rôle n'existe pas.")
        else:
            await ctx.send(f"Désolée, je ne connais pas cette commande ou celle-ci a plantée...\n{error}")
            print(f"**Command Error:**\n{ctx.message.content}")
            print(str(error))
    else:
        if str(error) == "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'channel'":
            await ctx.send("Tu dois être dans un salon vocal pour que je puisse me connecter.")
        elif str(error) == "arg is a required argument that is missing.":
            await ctx.send("Tu dois ajouter un argument pour cette commande.")
        elif str(error) == "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'id'":
            await ctx.message.author.send("Ce rôle n'existe pas.")
        else:
            await ctx.send("Désolée, je ne connais pas cette commande ou celle-ci a plantée...\n")
            print("**Command Error:**\n " + ctx.message.content)
            print(str(error))
        

# Start | YATTA !
bot.run(DISCORD_TOKEN)