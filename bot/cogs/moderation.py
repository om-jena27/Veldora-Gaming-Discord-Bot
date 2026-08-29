import discord
from discord.ext import commands
from discord import app_commands

class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Post an official server announcement embed (Admin/Mod only)")
    @app_commands.describe(
        title="Announcement Title",
        message="Announcement content/details",
        channel="Channel to post in (Defaults to current channel)",
        ping_everyone="Whether to ping @everyone"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def announce_slash(
        self,
        interaction: discord.Interaction,
        title: str,
        message: str,
        channel: discord.TextChannel = None,
        ping_everyone: bool = False
    ):
        target_channel = channel or interaction.channel

        embed = discord.Embed(
            title=f"📢 {title}",
            description=message,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Posted by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        embed.timestamp = discord.utils.utcnow()

        content = "@everyone" if ping_everyone else None

        await target_channel.send(content=content, embed=embed)
        await interaction.response.send_message(f"✅ Announcement posted in {target_channel.mention}!", ephemeral=True)

    @app_commands.command(name="post_rules", description="Post official server rules embed into current channel (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def post_rules_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📜 SERVER RULES & COMMUNITY GUIDELINES",
            description=(
                "Welcome to our gaming community! Please follow these guidelines to keep the server fun for everyone.\n\n"
                "**1️⃣ Respect Everyone**\nNo toxicity, hate speech, harassment, or personal attacks.\n\n"
                "**2️⃣ Voice Channel Etiquette**\nNo mic spamming or loud noise. Respect squad channel limits.\n\n"
                "**3️⃣ Fair Play & No Cheating**\nZero tolerance for cheating, hacking, or exploit abuse in any game.\n\n"
                "**4️⃣ Channel Usage & Spam**\nUse channels for their intended topics. Memes in `#meme-central`, bot commands in `#bot-commands`.\n\n"
                "**5️⃣ No Self-Promotion**\nDo not advertise streams or other Discord servers without permission."
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Head to #get-roles to select your gaming roles!")
        await interaction.response.send_message("Rules posted below!", ephemeral=True)
        await interaction.channel.send(embed=embed)

    @app_commands.command(name="clear", description="Clear/Purge messages from a channel (Admin/Mod only)")
    @app_commands.describe(amount="Number of messages to delete (1-100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_slash(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            await interaction.response.send_message("❌ Please specify an amount between 1 and 100.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🧹 Cleaned `{len(deleted)}` messages!", ephemeral=True)

    @app_commands.command(name="kick", description="Kick a member from the server (Mod/Admin only)")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 Kicked **{member.name}** | Reason: {reason}")

    @app_commands.command(name="ban", description="Ban a member from the server (Admin only)")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 Banned **{member.name}** | Reason: {reason}")


async def setup(bot: commands.Bot):
    await bot.add_cog(ModerationCog(bot))
