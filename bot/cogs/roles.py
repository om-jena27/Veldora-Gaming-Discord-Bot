import discord
from discord.ext import commands
from discord import app_commands

# --- Game Roles Dropdown ---
class GameRoleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Valorant", emoji="🎯", description="Get pinged for Valorant matches & LFG"),
            discord.SelectOption(label="Rocket League", emoji="🚗", description="Rocket League squad & casual play"),
            discord.SelectOption(label="BGMI", emoji="📱", description="Battlegrounds Mobile India rooms & squads"),
            discord.SelectOption(label="CS:GO", emoji="🔫", description="CS2 matchmaking & lobbies"),
            discord.SelectOption(label="Apex Legends", emoji="🔥", description="Apex Legends trios & squads"),
            discord.SelectOption(label="Minecraft", emoji="⛏️", description="Minecraft SMP & casual play"),
        ]
        super().__init__(
            placeholder="🎮 Select your Games...",
            min_values=0,
            max_values=len(options),
            options=options,
            custom_id="select_game_roles"
        )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        selected_games = self.values

        all_game_roles = ["Valorant", "Rocket League", "BGMI", "CS:GO", "Apex Legends", "Minecraft"]
        added = []
        removed = []

        for role_name in all_game_roles:
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                try:
                    role = await guild.create_role(name=role_name, reason="Created for Game Select Panel")
                except Exception:
                    continue

            if role_name in selected_games:
                if role not in member.roles:
                    await member.add_roles(role)
                    added.append(role_name)
            else:
                if role in member.roles:
                    await member.remove_roles(role)
                    removed.append(role_name)

        msg = []
        if added:
            msg.append(f"🟢 Added: **{', '.join(added)}**")
        if removed:
            msg.append(f"🔴 Removed: **{', '.join(removed)}**")
        if not msg:
            msg.append("ℹ️ No changes made to your game roles.")

        await interaction.response.send_message("\n".join(msg), ephemeral=True)


# --- Gamer Type & Playstyle Dropdown ---
class PlaystyleRoleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Competitive Gamer", emoji="🏆", description="Ranked & competitive play"),
            discord.SelectOption(label="Casual Gamer", emoji="🕹️", description="Fun & casual gaming"),
            discord.SelectOption(label="Streamer", emoji="🎥", description="Live streamer & content creator"),
        ]
        super().__init__(
            placeholder="🏆 Select your Gamer Style...",
            min_values=0,
            max_values=len(options),
            options=options,
            custom_id="select_playstyle_roles"
        )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        selected = self.values
        all_roles = ["Competitive Gamer", "Casual Gamer", "Streamer"]

        for role_name in all_roles:
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                try:
                    role = await guild.create_role(name=role_name, reason="Created for Playstyle Select Panel")
                except Exception:
                    continue

            if role_name in selected:
                if role not in member.roles:
                    await member.add_roles(role)
            else:
                if role in member.roles:
                    await member.remove_roles(role)

        await interaction.response.send_message("✅ Updated your Gamer Style roles!", ephemeral=True)


# --- Special Interests & Notifications Dropdown ---
class InterestRoleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Music Enthusiast", emoji="🎵", description="Music channels & bot access"),
            discord.SelectOption(label="Meme Lord", emoji="🤡", description="Meme sharing & auto memes"),
            discord.SelectOption(label="Event Notified", emoji="📢", description="Get pinged for server tournaments & events"),
        ]
        super().__init__(
            placeholder="🎵 Select your Interests...",
            min_values=0,
            max_values=len(options),
            options=options,
            custom_id="select_interest_roles"
        )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        selected = self.values
        all_roles = ["Music Enthusiast", "Meme Lord", "Event Notified"]

        for role_name in all_roles:
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                try:
                    role = await guild.create_role(name=role_name, reason="Created for Interest Select Panel")
                except Exception:
                    continue

            if role_name in selected:
                if role not in member.roles:
                    await member.add_roles(role)
            else:
                if role in member.roles:
                    await member.remove_roles(role)

        await interaction.response.send_message("✅ Updated your Interest & Notification roles!", ephemeral=True)


# --- Master View with all Dropdowns ---
class CategoryRolesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GameRoleSelect())
        self.add_item(PlaystyleRoleSelect())
        self.add_item(InterestRoleSelect())


class RolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="setup_roles")
    @commands.has_permissions(administrator=True)
    async def setup_roles(self, ctx: commands.Context):
        """Sends the Multi-Category Role Selector into the current channel."""
        embed = discord.Embed(
            title="🎮 COMMUNITY CATEGORY ROLES",
            description=(
                "Customize your profile by selecting roles from the dropdown menus below!\n\n"
                "🎯 **Games:** Valorant, Rocket League, BGMI, CS:GO, Apex, Minecraft\n"
                "🏆 **Playstyle:** Competitive Gamer, Casual Gamer, Streamer\n"
                "🎵 **Interests:** Music Enthusiast, Meme Lord, Event Notified"
            ),
            color=discord.Color.blurple()
        )
        embed.set_footer(text="Veldora Bot • Multi-Category Role Manager")
        await ctx.send(embed=embed, view=CategoryRolesView())
        await ctx.message.delete()

    @app_commands.command(name="rolepanel", description="Publish the category role selector dropdowns (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def rolepanel_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎮 COMMUNITY CATEGORY ROLES",
            description=(
                "Customize your profile by selecting roles from the dropdown menus below!\n\n"
                "🎯 **Games:** Valorant, Rocket League, BGMI, CS:GO, Apex, Minecraft\n"
                "🏆 **Playstyle:** Competitive Gamer, Casual Gamer, Streamer\n"
                "🎵 **Interests:** Music Enthusiast, Meme Lord, Event Notified"
            ),
            color=discord.Color.blurple()
        )
        embed.set_footer(text="Veldora Bot • Multi-Category Role Manager")
        await interaction.response.send_message("Role panel sent below!", ephemeral=True)
        await interaction.channel.send(embed=embed, view=CategoryRolesView())


async def setup(bot: commands.Bot):
    await bot.add_cog(RolesCog(bot))
    bot.add_view(CategoryRolesView())
