import os
from pathlib import Path
from dotenv import load_dotenv

# Search for .env in current directory (bot/.env) or root directory (Veldora/.env)
env_path = Path(__file__).parent / ".env"
parent_env_path = Path(__file__).parent.parent / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
elif parent_env_path.exists():
    load_dotenv(dotenv_path=parent_env_path)
else:
    load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "0"))
AUTO_ROLE_NAME = os.getenv("AUTO_ROLE_NAME", "Gamers")

# Supported games for role assignment and LFG
SUPPORTED_GAMES = {
    "valorant": {"name": "Valorant", "emoji": "🎯", "role_name": "Valorant"},
    "rocket_league": {"name": "Rocket League", "emoji": "🚗", "role_name": "Rocket League"},
    "bgmi": {"name": "BGMI / PUBG", "emoji": "📱", "role_name": "BGMI"},
    "cs2": {"name": "CS:GO / CS2", "emoji": "🔫", "role_name": "CS:GO"},
    "apex": {"name": "Apex Legends", "emoji": "🔥", "role_name": "Apex Legends"},
    "minecraft": {"name": "Minecraft", "emoji": "⛏️", "role_name": "Minecraft"},
}

SPECIAL_ROLES = {
    "music": {"name": "Music Enthusiast", "emoji": "🎵", "role_name": "Music Enthusiast"},
    "memes": {"name": "Meme Lord", "emoji": "🤡", "role_name": "Meme Lord"},
}
