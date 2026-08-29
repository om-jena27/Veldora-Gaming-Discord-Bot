import discord
from discord.ext import commands
import config

class WelcomeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild

        # 1. Auto-assign default Gamer role
        auto_role = discord.utils.get(guild.roles, name=config.AUTO_ROLE_NAME)
        if auto_role:
            try:
                await member.add_roles(auto_role)
            except Exception:
                pass

        # 2. Send Welcome Embed
        channel = None
        if config.WELCOME_CHANNEL_ID:
            channel = guild.get_channel(config.WELCOME_CHANNEL_ID)

        if not channel:
            # Fallback search for a channel named welcome
            channel = discord.utils.get(guild.text_channels, name="welcome-and-goodbye") or \
                      discord.utils.get(guild.text_channels, name="welcome")

        if channel:
            embed = discord.Embed(
                title=f"🎮 Welcome to {guild.name}, {member.name}!",
                description=(
                    f"Hey {member.mention}, glad to have you in the arena!\n\n"
                    "👉 Grab your gaming roles in **#get-roles**\n"
                    "👉 Check out **#rules-and-info**\n"
                    "👉 Hop into **#general-chat** or a voice channel and let's game!"
                ),
                color=discord.Color.purple()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Member #{guild.member_count}")
            await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(WelcomeCog(bot))
