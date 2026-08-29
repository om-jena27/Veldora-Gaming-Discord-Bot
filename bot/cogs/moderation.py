import discord
from discord.ext import commands
from discord import app_commands
import config

class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def send_rules_embed(self, channel: discord.TextChannel, guild: discord.Guild, author: discord.User = None):
        gamer_role = discord.utils.get(guild.roles, name=config.AUTO_ROLE_NAME) or discord.utils.get(guild.roles, name="Gamers")
        role_mention = gamer_role.mention if gamer_role else f"**@{config.AUTO_ROLE_NAME}**"

        embed = discord.Embed(
            title="📜 VELDORA GAMING COMMUNITY RULES & GUIDELINES",
            description=(
                f"Welcome to **{guild.name}**! Upon joining and verifying, members are assigned the {role_mention} role to access all community channels.\n\n"
                "Please read and follow our community guidelines to keep the server fun, competitive, and safe for everyone!"
            ),
            color=discord.Color.gold()
        )

        embed.add_field(
            name="👋 1. Verification & Member Access",
            value=f"All verified members receive the {role_mention} role. Head over to **#🏷️｜get_roles** to pick your games (Valorant, Rocket League, BGMI, CS:GO, Apex, Minecraft) and playstyle!",
            inline=False
        )

        embed.add_field(
            name="🤝 2. Respect & General Conduct",
            value="Treat all members with respect. Zero tolerance for toxicity, hate speech, racism, harassment, or personal attacks.",
            inline=False
        )

        embed.add_field(
            name="🎙️ 3. Voice Channel & Squad Etiquette",
            value="No mic spamming, ear-rape audio, or loud background noise. Use Push-to-Talk if needed. Respect squad channel user limits.",
            inline=False
        )

        embed.add_field(
            name="🎯 4. Fair Play & Anti-Cheat Policy",
            value="Strict zero-tolerance policy against hacks, cheats, exploits, or stream sniping. Cheaters will be permanently banned immediately.",
            inline=False
        )

        embed.add_field(
            name="💬 5. Text Channel Guidelines & Spam",
            value="Keep talk relevant: memes in **#🤡｜memes**, bot commands in **#🪩｜bot_commands**, game talk in game channels. No spamming or `@everyone` pings.",
            inline=False
        )

        embed.add_field(
            name="🚫 6. No Self-Promotion or Invite Links",
            value="Do not post unauthorized stream links, products, or Discord invite links in public text channels.",
            inline=False
        )

        embed.add_field(
            name="🛡️ 7. Support & Staff Assistance",
            value="If you need help or want to report a rule breaker, open a private ticket in **#🎯｜support_feedback**!",
            inline=False
        )

        embed.set_footer(text=f"{guild.name} • Official Guidelines", icon_url=guild.icon.url if guild.icon else None)
        embed.timestamp = discord.utils.utcnow()

        await channel.send(embed=embed)

    @commands.command(name="post_rules")
    @commands.has_permissions(administrator=True)
    async def post_rules_prefix(self, ctx: commands.Context):
        """Prefix command: !post_rules"""
        await self.send_rules_embed(ctx.channel, ctx.guild, ctx.author)
        try:
            await ctx.message.delete()
        except Exception:
            pass

    @app_commands.command(name="post_rules", description="Post official community rules embed with member role mention (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def post_rules_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await self.send_rules_embed(interaction.channel, interaction.guild, interaction.user)
        await interaction.followup.send("✅ Rules embed posted in this channel!", ephemeral=True)

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
