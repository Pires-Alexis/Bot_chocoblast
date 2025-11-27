# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import os                                                                                                                                                                                                          
from dotenv import load_dotenv
from pathlib import Path
import json
import pymysql
load_dotenv(Path("./.env"))
def load_data(filepath:str): #Load a json file
    with open(filepath, 'r') as file:
        return json.load(file)

conn = pymysql.connect(
    host=str(os.getenv("HOST")),
    user=str(os.getenv("USER")),
    password=str(os.getenv("PASSWORD_SQL")),
    database=str(os.getenv("USER"))+"$Chocoblast"
)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_pseudo` INT,
  `prenom` VARCHAR(255) NOT NULL,
  `chocoblast` INT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
)
conn.commit()

participants = load_data("data.json")
for entry in participants:
    cursor.execute(
        "INSERT INTO users (prenom, chocoblast, id_pseudo) VALUES (%s, %s, %s)",
        (entry["prenom"], entry["chocoblast"], entry["id_pseudo"])
    )
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "chocoblast" in message.content.lower().strip():
        await message.channel.send(f'<@{message.author.id}> s\'est fait chocoblast')
        cursor.execute("""
                       UPDATE users
SET chocoblast = chocoblast + 1
                       Where id_pseudo = %s ;
                       """,(message.author.id))
@bot.tree.command(name="ChocoList",description="Affiche les chocoblasts")
async def test(interaction: discord.Interaction,ctx):
    await cursor.execute("""
                         SELECT id_pseudo,chocoblast from users
                         """)
    ligne = cursor.fetchone()
    id_pseudo,nbr =ligne
    description = ""
    for i in ligne :
        descriptions += f'- <@{id_pseudo[i]}> : {nbr} chocoblast{"s" if nbr > 1 else ""} \n'
    embed  = discord.Embed(title = "Lists des joueurs aux Chocoblast",description=descriptions)
    interaction.response.send_message(embed=embed)

@bot.tree.command(name="ChocoClassemement",description="Affiche le classement des chocoblastés")
async def classe(interaction: discord.Integration):
    await cursor.execute("""
                         SELECT id_pseudo,chocoblast from users
                         """)
    scores = cursor.fetchone()
    classement = sorted(
    ((name, score) for name, score in scores if score > 0),
    key=lambda x: x[1],
    reverse=True
)


    # Couleurs dynamiques selon rang
    color_map = [discord.Color.gold(), discord.Color.dark_gray(), discord.Color.light_grey()]
    embed = discord.Embed(
        title="🏆 Classement des Scores",
        description="Voici les utilisateurs avec un score > 0",
        color=discord.Color.blue()  # couleur par défaut
    )

    for i, (name, score) in enumerate(classement, start=1):
        # Médaille top 3
        medal = ""
        if i == 1: 
            medal = "🥇 "
            embed.color = discord.Color.gold()
        elif i == 2: 
            medal = "🥈 "
            embed.color = discord.Color.dark_gray()
        elif i == 3: 
            medal = "🥉 "
            embed.color = discord.Color.light_grey()
    interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await bot.tree.sync() 
client.run(os.getenv("DISCORD_TOKEN"))
