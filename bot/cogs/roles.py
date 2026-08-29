import discord
from discord.ext import commands
from discord import app_commands

ALL_SERVER_ROLES = {
    "👑 Server Owner": discord.Color.gold(),
    "👑 Admin": discord.Color.dark_gold(),
    "🛡️ Moderator": discord.Color.red(),
    "🤖 Bot": discord.Color.dark_grey(),
    "💎 VIP Gamer": discord.Color.purple(),
    "Gamers": discord.Color.blue(),
    "Valorant": discord.Color.magenta(),
    "Rocket League": discord.Color.orange(),
    "BGMI": discord.Color.green(),
    "CS:GO": discord.Color.dark_orange(),
    "Apex Legends": discord.Color.dark_red(),
    "Minecraft": discord.Color.dark_green(),
    "Competitive Gamer": discord.Color.dark_purple(),
    "Casual Gamer": discord.Color.light_grey(),
    "Streamer": discord.Color.dark_magenta(),
    "Music Enthusiast": discord.Color.dark_teal(),
    "Meme Lord": discord.Color.teal(),
    "Event Notified": discord.Color.yellow(),
    "🥉 Level 5 - Rookie": discord.Color.from_rgb(205, 127, 50),
    "🥈 Level 15 - Veteran": discord.Color.from_rgb(192, 192, 192),
    "🥇 Level 30 - Elite": discord.Color.from_rgb(255, 215, 0),
    "👑 Level 50 - Legend": discord.Color.from_rgb(230, 0, 230)
}

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

    async def create_all_roles(self, guild: discord.Guild):
        added = []
        for role_name, color in ALL_SERVER_ROLES.items():
            existing = discord.utils.get(guild.roles, name=role_name)
            if not existing:
                try:
                    await guild.create_role(name=role_name, color=color)
                    added.append(role_name)
                except Exception:
                    pass
        return added

    @commands.command(name="setup_roles_all")
    @commands.has_permissions(administrator=True)
    async def setup_roles_all_cmd(self, ctx: commands.Context):
        """Prefix command: !setup_roles_all to create all 22 server roles."""
        added = await self.create_all_roles(ctx.guild)
        if added:
            await ctx.send(f"✅ Created {len(added)} missing server roles:\n**{', '.join(added)}**")
        else:
            await ctx.send("✅ All 22 server roles are already created and present in your server!")

    @app_commands.command(name="setup_roles_all", description="Create all 22 community server roles instantly (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_roles_all_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        added = await self.create_all_roles(interaction.guild)
        if added:
            await interaction.followup.send(f"✅ Created {len(added)} missing server roles:\n**{', '.join(added)}**", ephemeral=True)
        else:
            await interaction.followup.send("✅ All 22 server roles are already created and present in your server!", ephemeral=True)

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
