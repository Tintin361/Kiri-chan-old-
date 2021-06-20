import discord
from discord.ext import commands
import list_of_things
import not_important
import reddit as red
from termcolor import colored
import datetime
import random as rd

DISCORD_TOKEN = not_important.bot_token

client = discord.Client
bot = commands.Bot(command_prefix="-", help_command=None)

ver = "0.4.10"
user_id = 443113150599004161
listmod = list_of_things.rlist()
online_message = "toujours Reddit"

def get_time():
    now = datetime.datetime.now()

    time = now.strftime(":%M:%S")
    hours = now.strftime("%H")

    if hours == 24:
        hours -= 24

    def_time = str(hours) + time
    return def_time

@bot.event
async def on_ready():
    print('Connecté en tant que: ' + colored('{0.user}'.format(bot), "cyan") + " - Kiri-chan prête !")
    print("Version Discord.py: " + discord.__version__ + " - Version du bot: " + ver)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=online_message))

@bot.listen()
async def on_message(msg):
    username = await bot.fetch_user(msg.author.id)
    author = ""
    if msg.author.id == 789984188224110632:
        author = "Kiri-chan"
        color = "cyan"
    elif msg.author.id == 443113150599004161:
        author = "Tintin"
        color = "yellow"
    else:
        author = username
        color = "blue"
    if str(msg.content) == "":
        content = "[image]" 
    else:
        content = str(msg.content)
    print(colored(author, color) + ": " + content)
    if msg.author == bot.user:
        return
    global listmod

    try:
        if msg.author.id != 443113150599004161:
            if msg.channel.id == msg.author.dm_channel.id:
                user = await bot.fetch_user(443113150599004161)
                await user.send(str(author) + ":\n" + msg.content)
    except:
        pass

    hist = open("history.txt", "a")
    time = get_time()

    hist.write(time + " - " + str(username) + ": " + content + "\n")

    if msg.content.startswith("!!"):
        if msg.authorS.id in listmod:
            channel = bot.get_channel(789872360609284136)
            await msg.delete()
            await channel.send(msg.content[-(len(msg.content) - 2):])
        elif msg.author.id not in listmod:
            await msg.delete()

    if bot.user.mentioned_in(msg) and msg.mention_everyone is False:
        await msg.channel.send("Utilise -help pour voir la liste des commandes.")

@bot.command()
async def ping(ctx):
    await ctx.send("Latence: " + str(bot.latency * 1000) + " ms.")

@bot.command()
async def web(ctx):
    await ctx.message.delete()
    await ctx.send("Voici l'URL: http://91.174.152.111:35080/pnh/terre_plate/")

@bot.command()
async def jimmy(ctx):
    await ctx.message.delete()
    await ctx.send("Voici l'URL pour Jimmy et la kète du 11 Septembre:\nhttp://91.174.152.111:35080/pnh/jimmy")

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

    await ctx.send("Voici le dernier post sur r/" + sub_title + ":\n\n" + title + "\n" + url)

@bot.command()
async def hot(ctx, arg):
    await ctx.message.delete()
    try:
        red.last_post(arg)
    except:
        await ctx.send(
            "Désolée, je n'ai pas trouvé le subreddit... :mag_right:")
        return

    result = red.hot_post(arg)
    title = result[0]
    url = result[1]
    sub_title = result[2]

    await ctx.send("Voici un post sur r/" + sub_title + ":\n\n" + title + "\n" + url)

@bot.command()
async def fakehistory(ctx):
    await ctx.message.delete()

    result = red.fake_history()
    url = result[1]
    title = result[0]

    await ctx.send("Voici un post sur r/FakeHistoryPorn:\n\n" + title + "\n" + url)

@bot.command()
async def time(ctx):
    await ctx.message.delete()
    time = get_time()
    await ctx.send("Il est " + time)

@bot.command()
async def random_num(ctx, arg1: int, arg2: int):
    await ctx.message.delete()
    result = rd.randint(arg1, arg2)
    await ctx.send("J'ai choisis le nombre: " + str(result))

@bot.command()
async def pseudo(ctx, *arg):
    await ctx.message.delete()
    name = ' '.join(arg)
    await ctx.guild.get_member(bot.user.id).edit(nick=name)
    await ctx.send('Mon nouveau pseudo c\'est: ' + "**" + name + "**")

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
    await ctx.channel.send(ctx.author.mention +' J\'ai changé ton pseudo, c\'est maintenant: ' + "**" + name + "** !")

@bot.command()
async def help(ctx):
    await ctx.message.delete()
    if ctx.message.author.id in listmod:
        total_string = ""
        for i1 in list_of_things.commandes_modo():
            total_string += i1
        await ctx.send(total_string)
    else:
        total_string = ""
        for i2 in list_of_things.commandes_user():
            total_string += i2
        await ctx.send(total_string)

@bot.command()
async def getpp(ctx):
    if ctx.author.id in listmod:
        await ctx.message.delete()
        await ctx.author.send("Kirlia-chan - https://imgur.com/a/PtCzz0O")

@bot.command()
async def stop(ctx):
    if ctx.message.author.id in listmod:
        await ctx.channel.send('(***Baille***) J\'ai sommeil, à bientôt !')
        await ctx.message.delete()
        await bot.logout()
    else:
        await ctx.channel.send('Nan, je reste éveillée !')

@bot.command()
async def fs(ctx):
    if ctx.message.author.id in listmod:
        await ctx.message.delete()
        await bot.logout()

@bot.command()
async def info(ctx):
    await ctx.channel.send('Je suis une bot encore en développement créée par Tintin#0001 !')
    await ctx.message.delete()

@bot.command()
async def version(ctx):
    global ver
    await ctx.message.delete()
    await ctx.send("Je suis en version " + ver)

@bot.command()
async def online(ctx):
    if ctx.message.author.id in listmod:
        await ctx.message.delete()
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=online_message))

@bot.command()
async def idle(ctx):
    if ctx.author.id in listmod:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Splatoon 2 ou à Pokémon'))
        await ctx.message.delete()

@bot.command()
async def dnd(ctx):
    if ctx.author.id in listmod:
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name='un anime (c\'est sympa Assassination Classroom !)'))
        await ctx.message.delete()

@bot.command()
async def invisible(ctx):
    if ctx.author.id in listmod:
        await bot.change_presence(status=discord.Status.invisible)
        await ctx.message.delete()

@bot.command()
async def mp(ctx, *arg):
    if ctx.message.author.id in listmod:
        await ctx.message.delete()
        content = ' '.join(arg)
        global user_id
        user = await bot.fetch_user(user_id)
        try:
            await user.send(content)
        except:
            await ctx.send("Désolée, impossible d'envoyer le Message privé.")
    else:
        await ctx.message.delete()
        await ctx.message.send("Tu n'a pas le droit d'envoyer un Message Privé...")

@bot.command()
async def mp_set(ctx, arg):
    if ctx.message.author.id in listmod:
        await ctx.message.delete()
        global user_id
        user_id = int(arg)
    else:
        await ctx.message.delete()

@bot.event
async def on_command_error(ctx, error):
    if ctx.message.author.id in listmod:
        await ctx.send("Désolée, je ne connais pas cette commande...\n" + str(error))
        print("Command Error: " + ctx.message.content)
        print(str(error))

bot.run(DISCORD_TOKEN)