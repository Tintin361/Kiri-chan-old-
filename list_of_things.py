from random import choice

modo = [443113150599004161, 525302352132046848, 585178159151054887]

help_m = ["Voici la liste des commandes:\n",
"**-help** -> Affiche la liste des commandes\n",
"**-ping** -> Affiche la latence\n",
"**-poyo** -> Poyo !\n",
"**-pseudo** -> Change mon pseudo\n",
"**-nick** -> Change ton pseudo\n",
"**-info** -> Obtiens des infos sur moi\n",
"**-time** -> Je te donne l'heure\n",
"**-random_num** -> Je te donne un nombre aléatoire en deux valeurs\n",
"**-last** -> Obtiens le dernier post Reddit d'un subreddit\n",
"**-hot** -> Obtiens un post Reddit d'un subreddit\n",
"**-fakehistory** -> Retourne un post du sub Reddit r/FakeHistoryPorn\n",
"**-web** -> Je t'envoie l'adresse du site web de mon créateur\n",
"**-jimmy** -> Je t'envoie l'URL de Jimmy RPG\n",
"**-version** -> Obtiens le numéro de version\n\n",
"Ces commandes sont disponible que pour les modérateurs:\n",
"**-mp_set** -> Permet de définir à qui j'envoie le Message Privé\n",
"**-mp** -> J'envoie le contenu de ton message\n"
"**-online** -> Je suis connectée\n",
"**-idle** -> Je deviens inactive\n",
"**-dnd** -> Ne me dérange pas\n",
"**-invisible** -> Mais t\'es pas là, mais t\'es où ?\n",
"**-stop** -> Arrêt du bot\n",
"**-fs** -> Arrêt forcé du bot\n"]

help_u = ["Voici la liste des commandes:\n",
"**-help** -> Affiche la liste des commandes\n",
"**-ping** -> Affiche la latence\n",
"**-poyo** -> Poyo !\n",
"**-pseudo** -> Change mon pseudo\n",
"**-nick** -> Change ton pseudo\n",
"**-info** -> Obtiens des infos sur moi\n",
"**-time** -> Je te donne l'heure\n",
"**-random_num** -> Je te donne un nombre aléatoire en deux valeurs\n",
"**-last** -> Obtiens le dernier post Reddit d'un subreddit\n",
"**-hot** -> Obtiens un post Reddit d'un subreddit\n",
"**-fakehistory** -> Retourne un post du sub Reddit r/FakeHistoryPorn\n",
"**-web** -> Je t'envoie l'adresse du site web de mon créateur\n",
"**-jimmy** -> Je t'envoie l'URL de Jimmy RPG\n",
"**-version** -> Obtiens le numéro de version\n"]

def rlist():
  return modo

def commandes_modo():
  return help_m

def commandes_user():
  return help_u