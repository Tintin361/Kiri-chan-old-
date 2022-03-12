import discord
modo = [443113150599004161, 525302352132046848, 585178159151054887]

def rlist():
  return modo

def get_help():
  embedMsg = discord.Embed(title="Liste des commandes", description="Liste de toutes les catégories", color=0xffffff)
  embedMsg.add_field(name="<:reddit:794069835138596886> Reddit", value="-helpReddit", inline=False)
  embedMsg.add_field(name="<:youtube:316620060221374466> Youtube", value="-helpYoutube", inline=False)
  embedMsg.add_field(name=":robot: Features", value="-helpFeatures", inline=False)
  embedMsg.add_field(name=":screwdriver: Outils", value="-helpTools", inline=False)
  embedMsg.add_field(name="<:Modo:945135154131791912> Administratif", value="-helpAdmin", inline=False)

  return embedMsg

def get_help_reddit():
  embedMsg = discord.Embed(title="<:reddit:794069835138596886> Reddit", description="Liste des commandes pour Reddit", color=0xff4300)
  embedMsg.add_field(name="-last [nom du subreddit]", value="Obtiens le dernier post d'un subreddit")
  embedMsg.add_field(name="-hot [nom du subreddit]", value="Obtiens un post populaire au hasard d'un subreddit")
  embedMsg.add_field(name="-fakehistory", value="Retourne un post du subreddit r/FakeHistoryPorn")
  embedMsg.add_field(name="-wallpaper", value="Retourne un post du subreddit r/Wallpaper")
  embedMsg.add_field(name="-honkai", value="Affiche un post du subreddit r/Houkai3rd")
  embedMsg.add_field(name="-crappy", value="Affiche un post du subreddit r/CrappyDesign")
  embedMsg.add_field(name="-upvote", value="Upvote le dernier post que j'affiche")
  embedMsg.add_field(name="-score [post]", value="Affiche le score du post")

  return embedMsg

def get_help_youtube():
  embedMsg = discord.Embed(title="<:youtube:316620060221374466> Youtube", description="Liste des commandes pour Youtube", color=0xFF0000)
  embedMsg.add_field(name="-ytdl [format] [url]", value="Télécharge une vidéo Youtube (formats disponibles: MP3, OOG, MKV)")
  embedMsg.add_field(name="-play [recherche ou url]", value="Joue une musique depuis Youtube dans un salon vocal")
  embedMsg.add_field(name="-pause", value="Met en pause la musique")
  embedMsg.add_field(name="-stop", value="Arrête la musique en cours")
  embedMsg.add_field(name="-resume", value="Reprends la musique là où tu l'avais arrêtée")
  embedMsg.add_field(name="-cheh", value="Quand le karma est contre toi...")
  embedMsg.add_field(name="-dream", value="Joue la musique de Dream dans un salon vocal")
  embedMsg.add_field(name="-segs", value="SEEEEEGGGGGGSSS !")
  embedMsg.add_field(name="-disconnect", value="Je quitte le salon vocal")

  return embedMsg

def get_help_features():
  embedMsg = discord.Embed(title=":robot: Features", description="Liste des commandes pour les features", color=0xed8a09)
  embedMsg.add_field(name="-poyo", value="POYO !")
  embedMsg.add_field(name="-pseudo [pseudonyme]", value="Change mon pseudo")
  embedMsg.add_field(name="-nick [pseudonyme]", value="Change ton pseudo si j'ai les per")
  embedMsg.add_field(name="-datetime", value="Je te donne l'heure")
  embedMsg.add_field(name="-randomNum [valeur 1] [valeur 2]", value="Je te donne un nombre aléatoire entre deux valeurs")

  return embedMsg

def get_help_tools():
  embedMsg = discord.Embed(title=":screwdriver: Outils", description="Liste des commandes pour les outils", color=0x6d6d6d)
  embedMsg.add_field(name="-ping", value="Affiche la latence")
  embedMsg.add_field(name="-info", value="Obtiens des infos sur moi")
  embedMsg.add_field(name="-version", value="Obtiens le numéro de version")
  embedMsg.add_field(name="-github", value="Lien vers le repo sur GitHub.")
  
  return embedMsg

def get_help_admin():
  embedMsg = discord.Embed(title="<:Modo:945135154131791912> Administratif", description="Liste des commandes uniquement pour les modérateurs", color=0xff00fa)
  embedMsg.add_field(name="-mpSet [ID utilisateur]", value="Permet de définir à qui j'envoie le Message Privé")
  embedMsg.add_field(name="-mp [contenu du message]", value="J'envoie le contenu de ton message")
  embedMsg.add_field(name="-join", value="Je rejoins le salon vocal dans lequel tu est connecté")
  embedMsg.add_field(name="-online [type] [message]", value="Je suis connectée")
  embedMsg.add_field(name="-idle [type] [message]", value="Je deviens inactive")
  embedMsg.add_field(name="-dnd [type] [message]", value="Ne me dérange pas")
  embedMsg.add_field(name="-invisible", value="Mais t'es pas là, mais t'es où ?")
  embedMsg.add_field(name="-shutdown", value="Arrêt du bot")

  return embedMsg