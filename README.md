# 🎮 Gaming Discord Server Blueprint & Custom Bot Setup Guide

Welcome to your complete **Gaming Discord Server** setup guide and companion bot codebase! This repository contains everything required to create, organize, and automate a gaming community server for games like **Rocket League**, **Valorant**, **BGMI / PUBG**, **CS:GO / CS2**, and more.

---

## 📌 1. Discord Server Structure Blueprint

### **Roles Hierarchy (Top to Bottom)**
Create the following roles in `Server Settings -> Roles`:
1. `👑 Admin` - Full administrator privileges
2. `🛡️ Moderator` - Manage messages, kick/mute members
3. `🤖 Bot` - Assigned to all bots (Veldora Bot, Music Bots)
4. `🎮 Gamers` - Default role assigned to all members on join
5. **Game Roles** (Used for pings and LFG):
   - `🎯 Valorant`
   - `🚗 Rocket League`
   - `📱 BGMI`
   - `🔫 CS:GO`
   - `🔥 Apex Legends`
   - `⛏️ Minecraft`
6. **Special Interest Roles**:
   - `🎵 Music Enthusiast`
   - `🤡 Meme Lord`

---

### **Category & Channel Layout**

```text
📋 INFORMATION & WELCOME
 ├── 📜 # rules-and-info          (Read-only channel for server guidelines)
 ├── 🏷️ # get-roles                (Button UI for game/interest roles)
 └── 👋 # welcome-and-goodbye      (Automatic welcome greetings)

💬 COMMUNITY CHAT
 ├── 💬 # general-chat            (Main hangout text channel)
 ├── 📢 # announcements           (Important server updates)
 └── 🤖 # bot-commands            (Command interactions)

🎮 GAMING LOUNGE
 ├── 🎮 # gaming-discussion       (General gaming news & chat)
 ├── 🎯 # valorant                (Valorant chat, highlights & rank flex)
 ├── 🚗 # rocket-league           (Rocket League clips & trade/chat)
 ├── 📱 # bgmi                    (BGMI room codes, strategy & clips)
 └── 👥 # looking-for-group       (Use /lfg to assemble gaming squads)

🎉 FUN & MEDIA
 ├── 🤡 # meme-central            (Memes sharing & automatic bot memes)
 ├── 📷 # media-and-clips         (Game highlights & screenshot sharing)
 └── 💡 # suggestions             (Community recommendations)

🎵 MUSIC ZONE
 ├── 🎶 # music-chat              (Play music commands & queue management)
 └── 🎧 # music-vibes-vc          (Voice channel dedicated to music)

🔊 VOICE SQUADS
 ├── 🔊 General Lounge 1
 ├── 🔊 General Lounge 2
 ├── 🎯 Valorant Squad (5 Slots Limit)
 ├── 🚗 Rocket League (3 Slots Limit)
 └── 📱 BGMI Squad (4 Slots Limit)
```

---

## 🤖 2. Custom Bot Setup & Deployment

### Step 1: Create a Discord Bot Application
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** and name it `Veldora Gaming Bot` (or your preferred bot name).
3. Navigate to **Bot** tab on the left sidebar.
4. Enable the following **Privileged Gateway Intents**:
   - ✅ **PRESENCE INTENT**
   - ✅ **SERVER MEMBERS INTENT**
   - ✅ **MESSAGE CONTENT INTENT**
5. Click **Reset Token** and copy your **Bot Token** (keep it secret!).
6. Go to **OAuth2 -> URL Generator**:
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Administrator` (or `Manage Roles`, `Send Messages`, `Embed Links`, `Read Message History`).
   - Copy the generated invite link and open it in your browser to invite the bot to your server.

---

### Step 2: Configure Environment Variables
1. Rename `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and paste your Bot Token:
   ```env
   DISCORD_TOKEN=your_actual_bot_token_here
   BOT_PREFIX=!
   AUTO_ROLE_NAME=Gamers
   ```

---

### Step 3: Local Installation & Running
Make sure you have **Python 3.10+** installed.

```bash
# Navigate to the bot directory
cd bot

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

---

## 🛠️ 3. In-Server Configuration & Bot Commands

### **Setting Up Button / Reaction Roles**
1. Go to your `#get-roles` channel in Discord.
2. Run the slash command:
   ```text
   /rolepanel
   ```
   *Or administrator prefix command:*
   ```text
   !setup_roles
   ```
3. A sleek interactive embed with buttons will appear! Users can click buttons (`Valorant`, `Rocket League`, `BGMI`, `Music Enthusiast`, `Meme Lord`) to instantly assign or remove roles.

---

### **Setting Up Auto-Meme Posting**
1. Go to your `#meme-central` channel.
2. Run command:
   ```text
   !set_automeme
   ```
3. The bot will automatically fetch and post top memes from Reddit gaming subreddits every 2 hours!
4. Users can also manually request memes anytime anywhere using:
   ```text
   /meme [category]
   ```

---

### **Looking For Group (LFG) Squad Pings**
Users can find squadmates by running:
```text
/lfg game:Valorant needed:3 note:"Competitive Rank Push! VC 1"
```
```text
/lfg game:Rocket League needed:1 note:"Casual 2v2s"
```
The bot will mention `@Valorant` or `@Rocket League` role so interested friends get notified!

---

## 🎵 4. Dedicated Music Bot Setup Guide

Discord officially changed third-party audio policies, so adding verified Music Bots provides the smoothest 24/7 music experience for your server.

### Recommended Free Music Bots:
1. **Jockie Music** (Most popular & reliable multi-bot setup)
   - **Invite Link:** [https://jockiemusic.com](https://jockiemusic.com)
   - **Commands:** `m!play <song/link>`, `m!skip`, `m!queue`, `m!pause`
2. **FredBoat** (High quality & easy setup)
   - **Invite Link:** [https://fredboat.com](https://fredboat.com)
   - **Commands:** `;;play <song/link>`, `;;skip`, `;;queue`
3. **GreenBot** (Supports YouTube, Spotify, Soundcloud)
   - **Invite Link:** [https://greenbot.app](https://greenbot.app)
   - **Commands:** `/play`, `/skip`, `/queue`

### Setting Up Music Channel Permissions:
- Limit music commands to `#music-chat` so other text channels stay clean.
- Join `🎧 Music Vibes VC` voice channel, run `/play <song name>` in `#music-chat`, and enjoy 24/7 tunes with friends!

---

## 🚀 5. Free 24/7 Hosting Guide (Optional)

If you don't want to run the bot on your local computer 24/7, you can deploy it for free on **Render** or **Railway**:

### Hosting on Render (Worker Service):
1. Push this repository to GitHub.
2. Log into [Render.com](https://render.com) and click **New -> Background Worker**.
3. Connect your GitHub repository.
4. Set Build Command: `pip install -r bot/requirements.txt`
5. Set Start Command: `python bot/main.py`
6. Under **Environment Variables**, add `DISCORD_TOKEN` with your bot token.
7. Click **Create Background Worker**! Your bot is now online 24/7!
