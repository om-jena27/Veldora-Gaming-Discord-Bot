import asyncio
import os
import sys
import logging
import discord
from discord.ext import commands
import config

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(config.BOT_PREFIX),
    intents=intents,
    help_command=commands.DefaultHelpCommand()
)

initial_extensions = [
    "cogs.roles",
    "cogs.memes",
    "cogs.gaming",
    "cogs.welcome",
    "cogs.moderation",
    "cogs.auto_setup",
    "cogs.verify",
    "cogs.tickets",
    "cogs.automod",
    "cogs.levels"
]

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Rocket League | Valorant | BGMI"
        )
    )
    try:
        synced = await bot.tree.sync()
        logging.info(f"Synced {len(synced)} Slash Commands successfully!")
    except Exception as e:
        logging.error(f"Failed to sync slash commands: {e}")

async def main():
    async with bot:
        for extension in initial_extensions:
            try:
                await bot.load_extension(extension)
                logging.info(f"Loaded extension: {extension}")
            except Exception as e:
                logging.error(f"Failed to load extension {extension}: {e}")

        if not config.DISCORD_TOKEN:
            logging.error("No DISCORD_TOKEN found in environment variables or .env file!")
            sys.exit(1)

        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
