import discord
from discord.ext import commands
from discord import app_commands

class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="button_close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        await interaction.response.send_message("🔒 Closing ticket in 5 seconds...", ephemeral=False)
        await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.timedelta(seconds=5))
        await channel.delete(reason="Ticket closed by user/staff")


class TicketCreateView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Support Ticket", style=discord.ButtonStyle.primary, emoji="📩", custom_id="button_open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user

        # Search for ticket category or create one
        category = discord.utils.get(guild.categories, name="🎫 TICKETS")
        if not category:
            category = await guild.create_category("🎫 TICKETS")

        # Create private ticket channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        mod_role = discord.utils.get(guild.roles, name="🛡️ Moderator") or discord.utils.get(guild.roles, name="Admin")
        if mod_role:
            overwrites[mod_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        ticket_channel_name = f"ticket-{member.name.lower()}"
        existing_channel = discord.utils.get(category.text_channels, name=ticket_channel_name)
        if existing_channel:
            await interaction.response.send_message(f"⚠️ You already have an open ticket in {existing_channel.mention}!", ephemeral=True)
            return

        ticket_channel = await category.create_text_channel(
            name=ticket_channel_name,
            category=category,
            overwrites=overwrites,
            topic=f"Support ticket for {member.name}"
        )

        embed = discord.Embed(
            title=f"📩 Support Ticket for {member.name}",
            description="Thank you for reaching out! Please describe your issue or question, and our staff will assist you shortly.",
            color=discord.Color.gold()
        )
        embed.set_footer(text="Click 'Close Ticket' below when resolved.")

        await ticket_channel.send(content=f"Welcome {member.mention}! Staff ping: {mod_role.mention if mod_role else ''}", embed=embed, view=TicketCloseView())
        await interaction.response.send_message(f"✅ Ticket created! Head over to {ticket_channel.mention}.", ephemeral=True)


class TicketsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ticketpanel", description="Publish the support ticket creation panel in #support-ticket (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticketpanel_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎫 COMMUNITY SUPPORT & HELP TICKETS",
            description=(
                "Need help, want to report a rule breaker, or have a question for staff?\n\n"
                "Click the **📩 Open Support Ticket** button below to create a private channel with our staff!"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Public Community Support System")
        await interaction.response.send_message("Ticket panel sent!", ephemeral=True)
        await interaction.channel.send(embed=embed, view=TicketCreateView())


async def setup(bot: commands.Bot):
    await bot.add_cog(TicketsCog(bot))
    bot.add_view(TicketCreateView())
    bot.add_view(TicketCloseView())
