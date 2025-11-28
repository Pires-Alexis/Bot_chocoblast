# This example requires the 'message_content' intent.
import discord
from discord.ext import commands     
from discord import app_commands                                                                                                                                                                                              
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
        return None
    except json.JSONDecodeError:
        print(f"❌ Fichier JSON invalide : {filepath}")
        return None
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return None


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
                ele['nbr_chocoblast'] += 1
                is_added = True
                with open("./data.json", "w", encoding="utf-8") as fp:
                    json.dump(data,fp)
                break
        if not(is_added) :
            add_user(pseudo,id)
            add_chocoblast(pseudo,id)
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
        with open("./data.json", "w", encoding="utf-8") as fp:
         json.dump(data,fp)
    except FileNotFoundError:
        print("file not found")
        creer_file()
        add_user(pseudo,id)
    
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)
client = discord.Client(intents=intents)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
    async def setup_hook(self):
        await self.tree.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "chocoblast" in message.content.lower().strip():
        await message.channel.send(f'{message.author.display_name} s\'est fait chocoblast')
        data = load_data("./data.json","r")
        for dat in data :
            if dat["id_pseudo"] == message.author.id:
                add_chocoblast(message.author.name,message.author.id)
            else :
                creer_file()
                add_chocoblast(message.author.name,message.author.id)


@bot.tree.command(name="chocostat",description="Affiche les chocoblasts")
async def test(interaction: discord.Interaction):
    try:
        ligne = load_data("./data.json","r")
        id_pseudo,nbr =ligne
        descriptions = ""
        for i in ligne :
            descriptions += f'- <@{id_pseudo[i]}> : {nbr} chocoblast{"s" if nbr > 1 else ""} \n'
        embed  = discord.Embed(title = "Lists des joueurs aux Chocoblast",description=descriptions)
        await interaction.response.send_message(embed=embed)
    except FileNotFoundError :
        print("file not found")
        creer_file()
        interaction.response.send_message("Il n'y a personne sur la bdd")

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

# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')
#     await bot.tree.sync() 
client.run(os.getenv("DISCORD_TOKEN"))
