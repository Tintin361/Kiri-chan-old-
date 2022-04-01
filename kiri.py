# Importation de bibliothèques de Discord
import discord
from discord.ext import commands
# Bibliothèques pour Linux
import os
# Modules avec tous les mots de passe [que vous ne pouvez pas voir :)].
import tools.passwords as pwrd

# Variable pour le bot
ver_num = "2.0.0"
online_message = "Hello"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="-", help_command=None, intents=intents)

loaded_ext = dict()

# Pour enlever le Event loop is closed
@bot.event
async def on_ready():
  print('the bot has logged in successfuly')

# Permet de charger un module (Cog) dans ./cogs/
@bot.command()
async def load(ctx, extensions):
    try:
        bot.load_extension(f'cogs.{extensions}')
    except:
        await ctx.send(f"Impossible de charger le module **{extensions}**.")
        return
    loaded_ext[extensions] = True

# Permet de décharger un module (Cog) dans ./cogs/ 
@bot.command()
async def unload(ctx, extensions):
    try:
        bot.unload_extension(f'cogs.{extensions}')
    except:
        await ctx.send(f"Impossible de décharger le module **{extensions}**.")
        return
    loaded_ext[extensions] = False
    
# Permet de recharger un module (Cog) dans ./cogs/ 
@bot.command()
async def reload(ctx, extensions):
    await unload(ctx, extensions)
    await load(ctx, extensions)
    
@bot.command()
async def allReload(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            bot.unload_extension(f'cogs.{filename[:-3]}')
            bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
async def modules(ctx):
    l = list()
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py") and loaded_ext[filename[:-3]] == True:
            l.append(filename[:-3])
    await ctx.send(l)
    
def get_modules() -> list():
    l = list()
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py") and loaded_ext[filename[:-3]] == True:
            l.append(filename[:-3])
    return l

# Charge tous les modules pour démarrer le bot
for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')
        loaded_ext[filename[:-3]] = True

# YATTA - Démarre le bot
bot.run(pwrd.bot_token)