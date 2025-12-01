# This example requires the 'message_content' intent.
import discord
from discord.ext import commands                                                                                                                                                                                   
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import re
load_dotenv(Path("./.env"))
guilds = discord.Object(id=int(os.getenv("GUILD_ID")))
def load_data(filepath: str):
    """
    Fonction polyvalente pour lire ou écrire un fichier JSON.
    
    Arguments :
    - filepath : chemin du fichier JSON
    
    Retour :
    -retourne les données chargées du JSON
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
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
def change_chocoblast(id,index):
    """Change le compteur d'un utilisateur"""
    data = load_data()
    is_change = False

    for ele in data:
        if ele['id'] == id:
            ele['nbr_chocoblast'] += index
            is_change = True
            break

    if not is_change:
        add_user(id)
        return add_chocoblast(id,index)

    save_data(data)
def add_chocoblast(id) :
    '''
    incrémente de 1 le compteur de chocoblast de quelqu'un
    '''
    is_added = False
    try :
        data = load_data("data.json")
        for ele in data :
            if ele['id_pseudo'] == id :
                ele['chocoblast'] += 1
                is_added = True
                break
        save_data(data)
        if not(is_added) :
            add_user(id)
            return add_chocoblast(id)
    except FileNotFoundError:
        print("can't add : file does not exist")
        creer_file()
def add_user(id) :
    '''
    rajoute une personne au fichier data.json
    '''
    try :
        data = load_data("./data.json")   
        data.append({"chocoblast" : 0, "id_pseudo" : id})
        save_data(data)
    except FileNotFoundError:
        print("file not found")
        creer_file()
        add_user(id)
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
intents.members = True
bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    await bot.tree.sync(guild=guilds)
    print("Commande slash activé")
    guild = bot.get_guild(int(os.getenv("GUILD_ID")))
    ids = {member.id for member in guild.members}
    data = load_data("./data.json")
    # on récupère les ids déjà dans la db
    db_ids = {entry["id_pseudo"] for entry in data}
    # ids manquants = ids du serveur - ids déjà enregistrés
    missing = ids - db_ids
    for user_id in missing:
        if user_id == 1441027736343941142 :
            continue
        add_user(user_id)
    for cmd in bot.tree.get_commands():
        print(cmd.name)


    print(f"{len(missing)} utilisateurs ajoutés .\nUser mis à jour")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "chocoblast" in normalize_message(message.content) and len(normalize_message(message.content)) == 10 :
        await message.channel.send(f'{message.author.display_name} s\'est fait chocoblast')
        guild = bot.get_guild(int(os.getenv("GUILD_ID")))
        ids = [member.id for member in guild.members]
        if message.author.id in ids:
            add_chocoblast(message.author.id)
        else:
            add_user(message.author.id)
            add_chocoblast(message.author.id)




@bot.tree.command(name="chocostat",description="Affiche les chocoblasts")
async def test(interaction: discord.Interaction):
    try:
        ligne = load_data("./data.json")
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
        title="🏆 Classement des chocoblastés",
        description="Voici les utilisateurs chocoblastés",
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
        name = interaction.guild.get_member(name)
        embed.add_field(name=f'{medal} - {"quelqu'un d'autre" if name == None else name} ', value=f'{score} chocoblast{"s" if score > 1 else ""}', inline=False)

    await interaction.response.send_message(embed=embed)
@bot.tree.command(name="chocochange",description="[Admin]ajout et enleve le nombre chocoblast d'une personne")
async def change_values(interaction : discord.Interaction,name:discord.Member,ajout : int):
    data = load_data("./data.json")
    if interaction.user.guild_permissions.administrator or interaction.user.id == 597518397290315807 :
        for i in range(len(data)):
            if data[i]["id_pseudo"] == name.id :
                data[i]["chocoblast"] += ajout
        save_data(data=data)
        await interaction.response.send_message(f"Le compteur de <@{name.id}> a été changé.")
    else:
        await interaction.response.send_message (f'Vous n\'avez pas les droits d\'admin pour changer le nombre de chocoblast de cette personne')
    
@bot.tree.command(name="chocoset",description="[Admin]change le nombre chocoblast d'une personne")
async def change_values(interaction : discord.Interaction,name:discord.Member,nombre : int):
    data = load_data("./data.json")
    if interaction.user.guild_permissions.administrator or interaction.user.id == 597518397290315807 :
        for i in range(len(data)):
            if data[i]["id_pseudo"] == name.id :
                data[i]["chocoblast"] = nombre
            else:
                await interaction.response.send_message(f"Il n'y a pas d'utilisateur qui a ce nom/id")
        save_data(data=data)
        await interaction.response.send_message(f"Le compteur de <@{name.id}> a été changé.")
    else:
        await interaction.response.send_message (f'Vous n\'avez pas les droits d\'admin pour changer le nombre de chocoblast de cette personne')
    

    

    


bot.run(os.getenv("DISCORD_TOKEN"))


