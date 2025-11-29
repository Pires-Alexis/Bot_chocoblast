# This example requires the 'message_content' intent.
import discord
from discord.ext import commands                                                                                                                                                                                   
from dotenv import load_dotenv
from pathlib import Path
import os
import json
load_dotenv(Path("./.env"))
def load_data(filepath: str, mode: str = "r", data: Any = None):
    """
    Fonction polyvalente pour lire ou écrire un fichier JSON.
    
    Arguments :
    - filepath : chemin du fichier JSON
    - mode : "r" pour lecture, "w" pour écriture
    - data : objet Python à écrire si mode="w"
    
    Retour :
    - Si mode="r", retourne les données chargées du JSON
    """
    try:
        if mode == "r":
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        
        else:
            raise ValueError("Mode invalide ! Utilisez 'r' pour lecture ou 'w' pour écriture.")
    except FileNotFoundError:
        print(f"❌ Fichier introuvable : {filepath}")
        creer_file()
        return None
def save_data(data):
    """Écrit les données dans le JSON"""
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

def creer_file() :
     '''
     creer un fichier json nommé data.json
     '''
     with open("data.json", "w") as f:
        return json.dump([], f)
def add_chocoblast(pseudo,id) :
    '''
    incrémente de 1 le compteur de chocoblast de quelqu'un
    '''
    is_added = False
    try :
        data = load_data("data.json","r")
        for ele in data :
            if ele['id_pseudo'] == id :
                ele['chocoblast'] += 1
                is_added = True
                break
        save_data(data)
        if not(is_added) :
            add_user(pseudo,id)
            return add_chocoblast(pseudo,id)
    except FileNotFoundError:
        print("can't add : file does not exist")
        creer_file()
def add_user(pseudo,id) :
    '''
    rajoute une personne au fichier data.json
    '''
    try :
        data = load_data("./data.json","r")
        data.append({"pseudo" : str(pseudo),"nbr_chocoblast" : 0, "id_pseudo" : id})
        save_data(data)
    except FileNotFoundError:
        print("file not found")
        creer_file()
        add_user(pseudo,id)
    
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "chocoblast" in message.content.lower().strip():
        await message.channel.send(f'{message.author.display_name} s\'est fait chocoblast')
        data = load_data("./data.json","r")
        for dat in data :
            if dat["id_pseudo"] == message.author.id:
                add_chocoblast(message.author.name,message.author.id)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    await bot.tree.sync()
    print("Commande slash activé")

@bot.tree.command(name="chocostat",description="Affiche les chocoblasts")
async def test(interaction: discord.Interaction):
    try:
        ligne = load_data("./data.json","r")
        descriptions = ""
        for i in range(len(ligne)) :
            id_pseudo = ligne[i]["id_pseudo"]
            nbr = ligne[i]["chocoblast"]
            descriptions += f'- <@{id_pseudo}> : {nbr} chocoblast{"s" if nbr > 1 else ""} \n'
        embed  = discord.Embed(title = "Lists des joueurs aux Chocoblast",description=descriptions)
        await interaction.response.send_message(embed=embed)
    except FileNotFoundError :
        print("file not found")
        creer_file()
        await interaction.response.send_message("Il n'y a personne sur la bdd")

# @bot.tree.command(name="ChocoClassemement",description="Affiche le classement des chocoblastés")
# async def classe(interaction: discord.Integration):
#     await cursor.execute("""
#                          SELECT id_pseudo,chocoblast from users
#                          """)
#     scores = cursor.fetchone()
#     classement = sorted(
#     ((name, score) for name, score in scores if score > 0),
#     key=lambda x: x[1],
#     reverse=True
# )


#     # Couleurs dynamiques selon rang
#     color_map = [discord.Color.gold(), discord.Color.dark_gray(), discord.Color.light_grey()]
#     embed = discord.Embed(
#         title="🏆 Classement des Scores",
#         description="Voici les utilisateurs avec un score > 0",
#         color=discord.Color.blue()  # couleur par défaut
#     )

#     for i, (name, score) in enumerate(classement, start=1):
#         # Médaille top 3
#         medal = ""
#         if i == 1: 
#             medal = "🥇 "
#             embed.color = discord.Color.gold()
#         elif i == 2: 
#             medal = "🥈 "
#             embed.color = discord.Color.dark_gray()
#         elif i == 3: 
#             medal = "🥉 "
#             embed.color = discord.Color.light_grey()
#     interaction.response.send_message(embed=embed)
 
bot.run(os.getenv("DISCORD_TOKEN"))
