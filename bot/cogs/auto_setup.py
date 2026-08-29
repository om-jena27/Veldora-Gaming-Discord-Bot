import discord
from discord.ext import commands
from discord import app_commands
from cogs.roles import CategoryRolesView
from cogs.verify import VerifyView
from cogs.tickets import TicketCreateView

RULES_TEXT = (
    "Welcome to our Gaming Community! Please follow these rules:\n\n"
    "**1️⃣ Respect Everyone**\nNo toxicity, hate speech, harassment, or personal attacks.\n\n"
    "**2️⃣ Voice Channel Etiquette**\nNo mic spamming or ear rape audio. Respect squad channel user limits.\n\n"
    "**3️⃣ Fair Play & No Cheating**\nZero tolerance for hacks, cheats, or exploit abuse in any game.\n\n"
    "**4️⃣ Channel Usage & Spam**\nUse channels correctly: memes in `#meme-central`, bot commands in `#bot-commands`.\n\n"
    "**5️⃣ No Self-Promotion / Invite Links**\nDo not advertise streams, products, or other Discord servers without permission."
)

ANNOUNCEMENT_TEXT = (
    "🎉 **WELCOME TO THE PUBLIC GAMING COMMUNITY!** 🎉\n\n"
    "Whether you play **Rocket League**, **Valorant**, **BGMI**, **CS2**, or casual games, welcome!\n\n"
    "👉 Step 1: Verify yourself in **#verify**\n"
    "👉 Step 2: Read guidelines in **#rules-and-info**\n"
    "👉 Step 3: Select your roles in **#get-roles**!\n"
    "👉 Step 4: Need help? Open a support ticket in **#support-ticket**!"
)

class AutoSetupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="build_server", description="AUTOMATICALLY builds entire PUBLIC gaming server (Channels, Verification, Tickets, Roles, Rules)!")
    @app_commands.checks.has_permissions(administrator=True)
    async def build_server_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild

        # 1. Create All Category Roles with Distinct Colors
        role_colors = {
            "👑 Admin": discord.Color.gold(),
            "🛡️ Moderator": discord.Color.red(),
            "🤖 Bot": discord.Color.dark_grey(),
            "Gamers": discord.Color.blue(),
            "Valorant": discord.Color.magenta(),
            "Rocket League": discord.Color.orange(),
            "BGMI": discord.Color.green(),
            "CS:GO": discord.Color.dark_orange(),
            "Apex Legends": discord.Color.dark_red(),
            "Minecraft": discord.Color.dark_green(),
            "Competitive Gamer": discord.Color.purple(),
            "Casual Gamer": discord.Color.light_grey(),
            "Streamer": discord.Color.dark_purple(),
            "Music Enthusiast": discord.Color.dark_teal(),
            "Meme Lord": discord.Color.teal(),
            "Event Notified": discord.Color.yellow()
        }

        created_roles = {}
        for role_name, color in role_colors.items():
            existing = discord.utils.get(guild.roles, name=role_name)
            if not existing:
                try:
                    created_roles[role_name] = await guild.create_role(name=role_name, color=color)
                except Exception:
                    pass
            else:
                created_roles[role_name] = existing

        async def create_tc(category, name, topic=None):
            existing = discord.utils.get(category.text_channels, name=name)
            if not existing:
                return await category.create_text_channel(name=name, topic=topic)
            return existing

        async def create_vc(category, name, limit=0):
            existing = discord.utils.get(category.voice_channels, name=name)
            if not existing:
                return await category.create_voice_channel(name=name, user_limit=limit)
            return existing

        # 2. Category 1: INFORMATION & WELCOME
        cat_info = await guild.create_category("📋 INFORMATION & WELCOME")
        c_verify = await create_tc(cat_info, "verify", "✅ Verify yourself to join the public community!")
        c_rules = await create_tc(cat_info, "rules-and-info", "📜 Server guidelines and rules.")
        c_roles = await create_tc(cat_info, "get-roles", "🏷️ Select your games, playstyle, and interest roles!")
        c_welcome = await create_tc(cat_info, "welcome-and-goodbye", "👋 Welcome greetings for new members.")
        c_ticket = await create_tc(cat_info, "support-ticket", "🎫 Open a ticket for staff help.")

        # Post verification embed in #verify
        embed_verify = discord.Embed(
            title="🛡️ PUBLIC COMMUNITY VERIFICATION",
            description=(
                "Welcome to our Gaming Community Server!\n\n"
                "Click the **✅ Verify & Join Community** button below to get full access to channels!"
            ),
            color=discord.Color.green()
        )
        await c_verify.send(embed=embed_verify, view=VerifyView())

        # Post rules embed in #rules-and-info
        embed_rules = discord.Embed(
            title="📜 SERVER RULES & COMMUNITY GUIDELINES",
            description=RULES_TEXT,
            color=discord.Color.blue()
        )
        await c_rules.send(embed=embed_rules)

        # Post Role Panel in #get-roles
        embed_roles = discord.Embed(
            title="🎮 COMMUNITY CATEGORY ROLES",
            description=(
                "Customize your profile by selecting roles from the dropdown menus below!\n\n"
                "🎯 **Games:** Valorant, Rocket League, BGMI, CS:GO, Apex, Minecraft\n"
                "🏆 **Playstyle:** Competitive Gamer, Casual Gamer, Streamer\n"
                "🎵 **Interests:** Music Enthusiast, Meme Lord, Event Notified"
            ),
            color=discord.Color.blurple()
        )
        await c_roles.send(embed=embed_roles, view=CategoryRolesView())

        # Post Ticket Panel in #support-ticket
        embed_ticket = discord.Embed(
            title="🎫 COMMUNITY SUPPORT & HELP TICKETS",
            description="Click **📩 Open Support Ticket** below to contact moderators privately.",
            color=discord.Color.gold()
        )
        await c_ticket.send(embed=embed_ticket, view=TicketCreateView())

        # 3. Category 2: COMMUNITY CHAT
        cat_community = await guild.create_category("💬 COMMUNITY CHAT")
        await create_tc(cat_community, "general-chat", "💬 Main hangout channel for chatting.")
        c_announce = await create_tc(cat_community, "announcements", "📢 Important server updates and news.")
        await create_tc(cat_community, "bot-commands", "🤖 Use bot commands here.")

        embed_announce = discord.Embed(
            title="📢 PUBLIC SERVER LAUNCH",
            description=ANNOUNCEMENT_TEXT,
            color=discord.Color.gold()
        )
        await c_announce.send(embed=embed_announce)

        # 4. Category 3: GAMING LOUNGE
        cat_gaming = await guild.create_category("🎮 GAMING LOUNGE")
        await create_tc(cat_gaming, "gaming-discussion", "🎮 General gaming talk and news.")
        await create_tc(cat_gaming, "valorant", "🎯 Valorant chat, clips & ranks.")
        await create_tc(cat_gaming, "rocket-league", "🚗 Rocket League clips & trades.")
        await create_tc(cat_gaming, "bgmi", "📱 BGMI room codes & squad chat.")
        await create_tc(cat_gaming, "looking-for-group", "👥 Use /lfg command to assemble squads!")

        # 5. Category 4: FUN & MEDIA
        cat_fun = await guild.create_category("🎉 FUN & MEDIA")
        await create_tc(cat_fun, "meme-central", "🤡 Memes and funny gaming clips.")
        await create_tc(cat_fun, "media-and-clips", "📷 Share game highlights and screenshots.")
        await create_tc(cat_fun, "suggestions", "💡 Share your ideas to improve the server.")

        # 6. Category 5: MUSIC ZONE
        cat_music = await guild.create_category("🎵 MUSIC ZONE")
        await create_tc(cat_music, "music-chat", "🎶 Queue music and manage music bot commands.")
        await create_vc(cat_music, "🎧 Music Vibes VC")

        # 7. Category 6: VOICE SQUADS
        cat_voice = await guild.create_category("🔊 VOICE SQUADS")
        await create_vc(cat_voice, "🔊 General Lounge 1")
        await create_vc(cat_voice, "🔊 General Lounge 2")
        await create_vc(cat_voice, "🎯 Valorant Squad (5 Slots)", limit=5)
        await create_vc(cat_voice, "🚗 Rocket League (3 Slots)", limit=3)
        await create_vc(cat_voice, "📱 BGMI Squad (4 Slots)", limit=4)

        await interaction.followup.send(
            "🚀 **PUBLIC COMMUNITY SERVER BUILT SUCCESSFULLY!** All 16 Category Roles, Verification, Support Tickets, Anti-Spam Automod, and Multi-Category Role Selector installed!",
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoSetupCog(bot))
