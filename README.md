
# 🍫 Bot Chocoblast

Bot Chocoblast est un bot Discord permettant aux membres d’un serveur de s’envoyer des **chocoblasts** pour animer la communauté et créer des interactions ludiques.

---

## ✨ Fonctionnalités

- 🎯 Envoyer un **chocoblast** à un membre du serveur  
- 🏆 Afficher un **classement** des utilisateurs les plus chocoblatés
- 🧰 Administrier avec un compte administrateur les chocoblasts
- ⚙️ Commandes simples et lisibles  
- 🔐 Projet sous licence **AGPL-3.0**

---

## 📦 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Pires-Alexis/Bot_chocoblast.git
cd Bot_chocoblast
```

### 2. Installer les dépendances

```bash
npm install
```

*(Adapte cette commande si ton projet utilise un autre gestionnaire ou une autre stack.)*

### 3. Configuration

Créer un fichier `.env` à la racine du projet :

```env
DISCORD_TOKEN=ton_token_discord
CLIENT_ID = client_id
CLIENT_SECRET = client_secret
GUILD_ID = guild_discord
```

### 4. Lancer le bot

```bash
npm start
```

---

## 🧩 Commandes

| Commande              | Description                                   |
|-----------------------|-----------------------------------------------|
| `Chocoblast`          | Chocoblast une personne                       |
| `/chococlassement`    | Affiche le classement des chocoblasts         |
| `/chocohelp`          | Liste les commandes disponibles               |

---

## 🛠️ Technologies

- **Node.js**  
- **Discord.js**  
- **dotenv**  
- Autres dépendances selon l’implémentation

---

## 🤝 Contribution

Les contributions sont les bienvenues.  
Tu peux ouvrir une *issue* ou proposer une *pull request* pour suggérer des améliorations ou corriger des bugs.

---

