import discord
from discord.ext import commands
from discord import app_commands

class GamingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="lfg", description="Find squad mates for your game! Pings the game role.")
    @app_commands.describe(
        game="The game you are playing (Valorant, Rocket League, BGMI, etc.)",
        needed="Number of players needed",
        note="Any extra info (e.g., Competitive rank, Casual, Room Code, Discord VC)"
    )
    @app_commands.choices(game=[
        app_commands.Choice(name="🎯 Valorant", value="Valorant"),
        app_commands.Choice(name="🚗 Rocket League", value="Rocket League"),
        app_commands.Choice(name="📱 BGMI / PUBG", value="BGMI"),
        app_commands.Choice(name="🔫 CS:GO / CS2", value="CS:GO"),
        app_commands.Choice(name="🔥 Apex Legends", value="Apex Legends"),
        app_commands.Choice(name="⛏️ Minecraft", value="Minecraft"),
    ])
    async def lfg_slash(
        self,
        interaction: discord.Interaction,
        game: app_commands.Choice[str],
        needed: int,
        note: str = "Ready to play!"
    ):
        role_name = game.value
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name=role_name)

        role_mention = role.mention if role else f"**@{role_name}**"

        embed = discord.Embed(
            title=f"🎮 Looking For Group: {game.name}",
            description=f"**Host:** {interaction.user.mention}\n**Players Needed:** `{needed}`\n**Note/Details:** {note}",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text="Click to join voice channels or reply to squad up!")

        await interaction.response.send_message(
            content=f"📢 {role_mention} assemble! {interaction.user.mention} is looking for squadmates!",
            embed=embed
        )

    @commands.command(name="lfg")
    async def lfg_prefix(self, ctx: commands.Context, game_name: str, needed: int = 1, *, note: str = "Ready to play!"):
        """Find squad mates using prefix: !lfg Valorant 3 Competitve rank push"""
        role = discord.utils.get(ctx.guild.roles, name=game_name)
        role_mention = role.mention if role else f"**@{game_name}**"

        embed = discord.Embed(
            title=f"🎮 Looking For Group: {game_name.capitalize()}",
            description=f"**Host:** {ctx.author.mention}\n**Players Needed:** `{needed}`\n**Note/Details:** {note}",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="Join voice channels or reply to squad up!")

        await ctx.send(
            content=f"📢 {role_mention} assemble! {ctx.author.mention} is looking for squadmates!",
            embed=embed
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(GamingCog(bot))
