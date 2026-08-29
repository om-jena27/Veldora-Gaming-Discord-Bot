import discord
from discord.ext import commands
from discord import app_commands
import config

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify & Join Community", style=discord.ButtonStyle.success, emoji="✅", custom_id="button_verify_member")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user

        role = discord.utils.get(guild.roles, name=config.AUTO_ROLE_NAME)
        if not role:
            role = await guild.create_role(name=config.AUTO_ROLE_NAME, color=discord.Color.blue())

        if role in member.roles:
            await interaction.response.send_message("✅ You are already verified!", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(
                f"🎉 Welcome to the community, {member.mention}! You now have full access to channels.",
                ephemeral=True
            )


class VerifyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="verifypanel", description="Publish the verification button panel in #verify (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def verifypanel_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛡️ PUBLIC COMMUNITY VERIFICATION",
            description=(
                "Welcome to our Gaming Community Server!\n\n"
                "To protect our members from bots, spammers, and raids, please verify yourself below:\n\n"
                "1️⃣ Read our guidelines in **#rules-and-info**.\n"
                "2️⃣ Click the **✅ Verify & Join Community** button below.\n"
                "3️⃣ Head over to **#get-roles** to grab your game roles!\n\n"
                "By verifying, you agree to follow our community rules."
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="Veldora Gaming Community • Anti-Raid Protection")
        await interaction.response.send_message("Verification panel sent!", ephemeral=True)
        await interaction.channel.send(embed=embed, view=VerifyView())


async def setup(bot: commands.Bot):
    await bot.add_cog(VerifyCog(bot))
    bot.add_view(VerifyView())
