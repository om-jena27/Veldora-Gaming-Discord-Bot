import re
import discord
from discord.ext import commands

INVITE_REGEX = re.compile(r"(discord\.gg|discord\.com/invite|discordapp\.com/invite)/[a-zA-Z0-9]+")

class AutomodCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        # Skip staff members
        if message.author.guild_permissions.manage_messages:
            return

        # Anti-Invite Link Protection in Public Chat
        if INVITE_REGEX.search(message.content):
            try:
                await message.delete()
                warning_msg = await message.channel.send(
                    f"⚠️ {message.author.mention}, self-promotion and unauthorized Discord invite links are not allowed in this public community server!"
                )
                await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.timedelta(seconds=5))
                await warning_msg.delete()
            except Exception:
                pass


async def setup(bot: commands.Bot):
    await bot.add_cog(AutomodCog(bot))
