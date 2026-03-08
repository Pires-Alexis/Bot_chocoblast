# This example requires the 'message_content' intent.
import discord
from discord.ext import commands                                                                                                                                                                                   
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import re
import locale
from datetime import datetime
load_dotenv(Path("./.env"))
locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

guild_id = int(os.getenv("GUILD_ID")) #avoir l'id du guild
guild_obj = discord.Object(id=guild_id)#en faire un object
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
def add_chocoblast(id,datetiming) :
    '''
    incrémente de 1 le compteur de chocoblast de quelqu'un
    '''
    is_added = False
    try :
        data = load_data("data.json")
        for ele in data :
            if ele['id_pseudo'] == id :
                ele['chocoblast'] += 1
                ele['datetime']=datetiming
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
        data.append({"chocoblast" : 0, "id_pseudo" : id,"datetime":None,"taxes":0})
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
    msg = re.sub(r"[^a-z0-9]", " ", msg)
    msg = msg.replace("0", "o").replace("1", "l").replace("4", "a").replace("'"," ")
    msg = msg.replace("eau", "o").replace("au", "o").replace("ç","c").replace("ô","o").replace("é","e")
    return msg

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event
async def on_ready(): 
    guild_bot = bot.get_guild(guild_id) #donner le guild au bot

    try:
        synced = await bot.tree.sync(guild=guild_obj)
        print(f"Commandes synchronisées : {len(synced)}")
    except Exception as e:
        print(f"Erreur de sync : {e}")


    ids = {member.id for member in guild_bot.members}
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


    print(f"{len(missing)-1} utilisateurs ajoutés .\nUser mis à jour")

    # Dictionnaire pour stocker l'état de chaque utilisateur
user_state = {}

# Définition des étapes de la conversation
STEPS = {
    "start": 0,
    "hello": 1,
    "bad_mood": 2,
    "alone": 3,
    "negative_reply": 4,
    "cv_pas": 5,
    "working":6
}
@bot.event
async def on_message(message):
    if message.author == bot.user: #pour pas qu'il se répond à lui même
        return
    user_id = int(message.author.id)
    content = normalize_message(message.content)

    # Initialiser l'état si l'utilisateur n'existe pas
    if user_id not in user_state:
        user_state[user_id] = STEPS["start"]
        

    # --- Gestion des messages ---
    elif ("slt" in content or "salut" in content or "hello" in content or "salam" in content) and user_state[user_id] == 0:
        await message.add_reaction("👋")
        user_state[user_id] = STEPS["hello"]
        await message.channel.send(f"Salut <@{user_id}> ! 👋\nÇa va ?")
    elif ("cv pas" in content) and int(user_state[user_id]) == 1:
        user_state[user_id] = STEPS["cv_pas"]
        await message.channel.send("Qu'est ce qui ne va pas ?")

    elif "tu marches pas" in content and user_state[user_id] == 5 :
        await message.channel.send(f"<@597518397290315807>, <@{user_id}> m'a dit que je me suis blessé")
    elif ("j aime pas vivre" in content or"j aime pas la vie" in content) and user_state[user_id] == 5:
        user_state[user_id] = STEPS["bad_mood"]
        await message.channel.send(
            "Je suis vraiment désolé que tu te sentes comme ça."
            "Même si je ne suis qu’un bot, tu n’es pas seul. "
            "Parler à quelqu’un en qui tu as confiance peut vraiment aider. "
            )

    elif ("je n ai personne" in content or "j ai personne a mes cote" in content) and user_state[user_id] == 2 :
        user_state[user_id] = STEPS["alone"]
        await message.channel.send(
            "Je suis désolé que tu te sentes seul… "
            "Même si je ne peux pas remplacer une vraie présence, je suis là pour te parler autant que tu veux. 💛"
        )

    elif content == "non" and user_state[user_id] == 3:
        user_state[user_id] = STEPS["negative_reply"]
        await message.channel.send(
            "D’accord… merci de m’avoir répondu. "
            "Tu mérites d’être entouré et soutenu, même si tu n’as pas l’impression que quelqu’un est là. 💛"
        )
    elif content == "tu marches" and user_state[user_id] == 1:
        await message.channel.send("oui,pk?")
        user_state[user_id] = STEPS["working"]
    elif content == "askip tu marches pas" and user_state[user_id] == 6 :
        await message.channel.send("Celui qui a dit ça est juste con trql")
        user_state[user_id] = STEPS ["start"]
    elif content == "oui" and user_state[user_id] == 1 :
        await message.channel.send("noice !!")
        user_state[user_id] = STEPS["start"]
    elif content == "non" and user_state[user_id] == 1 :
        await message.channel.send ("En vrai,j'espère que ça ira mieux..")
        user_state[user_id] = STEPS["start"]
    elif content == "tg" and user_state[user_id] == 1:
        await message.channel.send("français")
        user_state[user_id] = STEPS["start"]

    # --- Si aucun cas ne correspond, on réinitialise l'état à start ---
    else :
        if user_state[user_id] != STEPS["start"]:
            print("Reset automatique : message hors sujet")
            user_state[user_id] = STEPS["start"]
    await bot.process_commands(message)
    if "chocoblast" in normalize_message(message.content) and len(normalize_message(message.content)) == 10 :
        await message.channel.send(f'{message.author.display_name} s\'est fait chocoblast')
        guild = bot.get_guild(int(os.getenv("GUILD_ID")))
        ids = [member.id for member in guild.members]
        if message.author.id in ids:
            add_chocoblast(message.author.id,message.created_at.isoformat())
        else:
            add_user(message.author.id)
            add_chocoblast(message.author.id,message.created_at.isoformat())




@bot.tree.command(name="chocostat",description="Affiche les chocoblasts",guild=guild_obj)
async def test(interaction: discord.Interaction):
    try:
        ligne = load_data("./data.json")
        descriptions = ""
        for i in range(len(ligne)) :
            id_pseudo = ligne[i]["id_pseudo"]
            nbr = ligne[i]["chocoblast"]
            taxe = ligne[i]["taxes"]
            dif = nbr - taxe    
            dt_value = ligne[i]["datetime"]
            if dt_value is not None:
             dattime = datetime.fromisoformat(dt_value)
            else:
             dattime = None  # ou gérer comme tu veux
            descriptions += f'- <@{id_pseudo}> : {nbr} chocoblast{"s" if nbr > 1 else ""}  {"" if dattime == None else f'\ndernier chocoblast :{dattime}\nChocoblast restant à payer : {dif}'} \n \n'
        embed  = discord.Embed(title = "Lists des joueurs au Chocoblast",description=descriptions,color=0xffa200)
        await interaction.response.send_message(embed=embed)
    except FileNotFoundError :
        print("file not found")
        creer_file()
        await interaction.response.send_message("Il n'y a personne sur la bdd.")

@bot.tree.command(name="chococlassement", description="Affiche le classement des chocoblastés",guild=guild_obj)
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
        color=0xffa200
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
@bot.tree.command(name="chocochange",description="[Admin]ajout et enleve le nombre chocoblast d'une personne",guild=guild_obj)
async def change_values(interaction : discord.Interaction,name:discord.Member,ajout : int):
    data = load_data("./data.json")
    if interaction.user.guild_permissions.administrator or interaction.user.id == 597518397290315807 :
        for i in range(len(data)):
            if data[i]["id_pseudo"] == name.id :
                data[i]["chocoblast"] += ajout
        save_data(data=data)
        await interaction.response.send_message(f"Le compteur de <@{name.id}> a été changé.")
    else:
        await interaction.response.send_message (f'Vous n\'avez pas les droits d\'admin pour changer le nombre de chocoblast de cette personne.')
    
@bot.tree.command(name="chocoset",description="[Admin]change le nombre chocoblast d'une personne.",guild=guild_obj)
async def change_values(interaction : discord.Interaction,name:discord.Member,nombre : int):
    found = False
    data = load_data("./data.json")
    if interaction.user.guild_permissions.administrator or interaction.user.id == 597518397290315807 :
        for i in range(len(data)):
            if int(data[i]["id_pseudo"]) == name.id :
                found = True
                data[i]["chocoblast"] = nombre
                break
        if not found :
            await interaction.response.send_message(f"Il n'y a pas d'utilisateur qui a ce nom/id.")
        else:
            await interaction.response.send_message(f"Le compteur de <@{name.id}> a été changé.")
        save_data(data=data)
    else:
        await interaction.response.send_message (f'Vous n\'avez pas les droits d\'admin pour changer le nombre de chocoblast de cette personne.')

@bot.tree.command(name="chocodate",description="[Admin]Change la date du dernier chocoblast d\'une personne",guild=guild_obj)
async def date(interaction:discord.Interaction,name:discord.Member,annee:int,mois:int,jour:int,heure:int,minutes:int):
    try:
        found = False
        data = load_data("./data.json")
        if interaction.user.guild_permissions.administrator or interaction.user.id == 597518397290315807 :
            for i in range(len(data)):
                if int(data[i]["id_pseudo"]) == name.id :
                    found = True
                    data[i]["datetime"] = str(datetime(annee, mois, jour, heure, minutes).isoformat())
                    break
            if not found :
                await interaction.response.send_message(f"Il n'y a pas d'utilisateur qui a ce nom/id.")
            else:
                await interaction.response.send_message(f"La date/time du dernier chocoblast de <@{name.id}> a été changé.")
            save_data(data=data)
        else:
            await interaction.response.send_message (f'Vous n\'avez pas les droits d\'admin pour changer la date/heure du dernier chocoblast de cette personne.')
    except ValueError :
        await interaction.response.send_message(f'Veuillez entrer des bonnes valeurs pour la date et l\'heure en chiffre.',ephemeral=True)
    except OverflowError :
        await interaction.response.send_message(f'Veuillez entrer des bonnes valeurs pour la date et l\'heure en chiffre.',ephemeral=True)
@bot.tree.command(name="chocohelp",description="Affiche l'aide pour le Chocobot",guild=guild_obj)
async def help(interaction:discord.Interaction):
    embed=discord.Embed(title="Aides Bot Chocoblast", description="Cette commande permet de vous aider à utiliser le bot Chocoblast.\nSi [Admin] est mentionné,vous devez être un administrateur pour exécuter la commandes",color=0xffa200)
    embed.add_field(name="Chocoblasting :", value="Ecrire \"chocoblast\" sur le compte discord de la personne en présence du bot augmente le nombre de chocoblast et le chocoblaster devra amener des chocolatines au plus vite pour payer sa dette", inline=False)
    embed.add_field(name="/chocostat", value="Voir toutes les personnes et leurs nombre de chocoblast", inline=False)
    embed.add_field(name="/chocohelp", value="Affiche ce champ", inline=False)
    embed.add_field(name="/chococlassement", value="Classement des chocoblastés", inline=False)
    embed.add_field(name="/chocoset", value=" [Admin] Met un certain nombre de chocoblast à une personne", inline=False)
    embed.add_field(name="/chocochange", value="[Admin] Ajoute (ou enlève) un certain nombre de chocoblast à une personne", inline=False)
    embed.add_field(name="/chocodate", value="[Admin] Change la date du dernier chocoblast d'une personne", inline=False)
    embed.add_field(name="/chocotax",value="[Admin]Valide la taxe d\'un certain nombre de chocoblast d'un utilisateur",inline=False)
    button = discord.ui.Button(
    label="Règlement officiel du chocoblast",
    url="https://www.chocoblast.fr/"
    )

    view = discord.ui.View()
    view.add_item(button)
    await interaction.response.send_message(embed=embed,view=view)

@bot.tree.command(name="chocotax",description="[Admin]Valide la taxe d\'un certain nombre de chocoblast d'un utilisateur",guild=guild_obj)
async def taxes(interaction:discord.Interaction,name:discord.Member,index:int):
    data = load_data("./data.json")
    if interaction.user.guild_permissions.administrator or interaction.user.id == 597518397290315807:
        for i in range(len(data)):
            if int(data[i]["id_pseudo"]) == name.id :
                found = True
                data[i]["taxes"] += index
                break
        if not found :
            await interaction.response.send_message(f"Il n'y a pas d'utilisateur qui a ce nom/id.")
        else:
            await interaction.response.send_message(f"Le compteur de <@{name.id}> a été changé.")
        save_data(data=data)

bot.run(os.getenv("DISCORD_TOKEN"))