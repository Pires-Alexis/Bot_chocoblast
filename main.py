# This example requires the 'message_content' intent.
import discord
from discord.ext import commands                                                                                                                                                                                   
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import re
load_dotenv(Path("./.env"))
guild = discord.Object(id=int(os.getenv("GUILD_ID")))
def load_data(filepath: str, mode: str = "r"):
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
def normalize_message(msg:str) -> str:
    """
    Rends les messages plus lisible, et utilisable
    """
    msg = msg.lower().strip()
    msg = re.sub(r"[^a-z0-9]", "", msg)
    msg = msg.replace("0", "o").replace("1", "l").replace("4", "a")
    msg = msg.replace("eau", "o").replace("au", "o")
    return msg
    
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "chocoblast" in normalize_message(message.content) and len(normalize_message(message.content)) == 10 :
        await message.channel.send(f'{message.author.display_name} s\'est fait chocoblast')
        data = load_data("./data.json","r")
        for dat in data :
            if dat["id_pseudo"] == message.author.id:
                add_chocoblast(message.author.name,message.author.id)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    await bot.tree.sync(guild=guild)
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
        embed  = discord.Embed(title = "Lists des joueurs au Chocoblast",description=descriptions,color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)
    except FileNotFoundError :
        print("file not found")
        creer_file()
        await interaction.response.send_message("Il n'y a personne sur la bdd")

@bot.tree.command(name="chococlassement", description="Affiche le classement des chocoblastés")
async def classe(interaction: discord.Interaction):
    scores = load_data("./data.json")
    
    # Filtre et tri
    classement = sorted(
        ((entry["id_pseudo"], entry["chocoblast"]) for entry in scores if entry["chocoblast"] > 0),
        key=lambda x: x[1],
        reverse=True
    )

    # Création de l'embed
    embed = discord.Embed(
        title="🏆 Classement des Scores",
        description="Voici les utilisateurs avec un score > 0",
        color=discord.Color.gold()
    )

    # Remplissage de l'embed
    for i, (name, score) in enumerate(classement, start=1):
        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"
        else:
            medal = f"{i}️⃣"

        embed.add_field(name=f"{medal} - <@{name}>", value=f"{score} chocoblast{"s" if score > 1 else ""}", inline=False)

    await interaction.response.send_message(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
