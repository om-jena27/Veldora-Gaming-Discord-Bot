import os
import discord
from discord.ext import commands
from discord import app_commands
import config

FALLBACK_BANNER_GIF = "https://i.gifer.com/76DY.gif"

class WelcomeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_welcome_image(self):
        """Checks for local custom Veldora banner in bot/assets/ supporting gif, mp4, png, jpg."""
        assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        
        possible_files = [
            "welcome_banner.gif.mp4",
            "welcome_banner.mp4",
            "welcome_banner.gif",
            "welcome_banner.png",
            "welcome_banner.jpg",
            "welcome_banner.jpeg"
        ]

        for fname in possible_files:
            fpath = os.path.join(assets_dir, fname)
            if os.path.exists(fpath):
                ext = fname.split(".")[-1].lower()
                if ext == "mp4":
                    return discord.File(fpath, filename=fname), None
                else:
                    return discord.File(fpath, filename=fname), f"attachment://{fname}"

        return None, FALLBACK_BANNER_GIF

    async def send_welcome_card(self, channel: discord.TextChannel, member: discord.Member):
        guild = member.guild

        guidelines_channel = discord.utils.get(guild.text_channels, name="📑｜guidelines")
        roles_channel = discord.utils.get(guild.text_channels, name="🏷️｜get_roles")
        chat_channel = discord.utils.get(guild.text_channels, name="💎｜general_chat")

        g_tag = guidelines_channel.mention if guidelines_channel else "**#guidelines**"
        r_tag = roles_channel.mention if roles_channel else "**#get_roles**"
        c_tag = chat_channel.mention if chat_channel else "**#general_chat**"

        embed = discord.Embed(
            title=f"🎮 WELCOME TO {guild.name.upper()}, {member.display_name.upper()}! 🎉",
            description=(
                f"Hey {member.mention}, welcome to the Veldora arena! We're thrilled to have you here.\n\n"
                f"📌 **Step 1:** Read our guidelines in {g_tag}\n"
                f"📌 **Step 2:** Pick your game roles (Valorant, BGMI, Rocket League) in {r_tag}\n"
                f"📌 **Step 3:** Say hello & squad up in {c_tag}!\n\n"
                "──────────────────────────────────────────────"
            ),
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        file_obj, img_url = self.get_welcome_image()
        if img_url:
            embed.set_image(url=img_url)

        embed.set_footer(text=f"Member #{guild.member_count} • {guild.name}", icon_url=guild.icon.url if guild.icon else None)
        embed.timestamp = discord.utils.utcnow()

        if file_obj:
            await channel.send(content=f"👋 Welcome to the server, {member.mention}!", embed=embed, file=file_obj)
        else:
            await channel.send(content=f"👋 Welcome to the server, {member.mention}!", embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild

        # 1. Auto-assign default Gamer role
        auto_role = discord.utils.get(guild.roles, name=config.AUTO_ROLE_NAME) or discord.utils.get(guild.roles, name="Gamers")
        if auto_role:
            try:
                await member.add_roles(auto_role)
            except Exception:
                pass

        # 2. Find welcome channel
        welcome_channel = (
            discord.utils.get(guild.text_channels, name="👋｜welcome") or
            discord.utils.get(guild.text_channels, name="welcome-and-goodbye") or
            discord.utils.get(guild.text_channels, name="welcome")
        )

        if welcome_channel:
            await self.send_welcome_card(welcome_channel, member)

    @commands.command(name="setup_welcome")
    @commands.has_permissions(administrator=True)
    async def setup_welcome_cmd(self, ctx: commands.Context):
        """Creates #👋｜welcome channel and posts the welcome card."""
        guild = ctx.guild

        category = discord.utils.get(guild.categories, name="✦─────⦅ WELCOME AREA ⦆─────✦")
        if not category:
            category = await guild.create_category("✦─────⦅ WELCOME AREA ⦆─────✦")

        welcome_channel = discord.utils.get(guild.text_channels, name="👋｜welcome")
        if not welcome_channel:
            welcome_channel = await category.create_text_channel(
                name="👋｜welcome",
                topic="👋 Official welcome channel for new community members!"
            )

        await self.send_welcome_card(welcome_channel, ctx.author)
        await ctx.send(f"✅ Created {welcome_channel.mention} and posted your animated welcome card!")

    @app_commands.command(name="setup_welcome", description="Create #👋｜welcome channel and post animated welcome card (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_welcome_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild

        category = discord.utils.get(guild.categories, name="✦─────⦅ WELCOME AREA ⦆─────✦")
        if not category:
            category = await guild.create_category("✦─────⦅ WELCOME AREA ⦆─────✦")

        welcome_channel = discord.utils.get(guild.text_channels, name="👋｜welcome")
        if not welcome_channel:
            welcome_channel = await category.create_text_channel(
                name="👋｜welcome",
                topic="👋 Official welcome channel for new community members!"
            )

        await self.send_welcome_card(welcome_channel, interaction.user)
        await interaction.followup.send(f"✅ Created {welcome_channel.mention} and posted your animated welcome card!", ephemeral=True)

    @commands.command(name="test_welcome")
    @commands.has_permissions(administrator=True)
    async def test_welcome_cmd(self, ctx: commands.Context):
        """Simulates a welcome message in the current channel."""
        await self.send_welcome_card(ctx.channel, ctx.author)


async def setup(bot: commands.Bot):
    await bot.add_cog(WelcomeCog(bot))
