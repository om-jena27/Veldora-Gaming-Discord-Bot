import discord
from discord.ext import commands
from discord import app_commands
from cogs.roles import CategoryRolesView
from cogs.verify import VerifyView
from cogs.tickets import TicketCreateView

GUIDELINES_TEXT = (
    "Welcome to the Community Server! Please follow our server guidelines:\n\n"
    "**1️⃣ Be Respectful**\nNo toxic behavior, harassment, hate speech, or offensive language.\n\n"
    "**2️⃣ Voice Channel Rules**\nNo loud noise, mic spamming, or ear-rape audio. Use Push-to-Talk if your background is noisy.\n\n"
    "**3️⃣ Fair Gaming & No Cheats**\nCheating, hacking, or exploiting in games is strictly prohibited.\n\n"
    "**4️⃣ Channel Usage**\nKeep discussions in relevant channels: memes in `#🤡 | memes`, bot commands in `#🪩 | bot_commands`.\n\n"
    "**5️⃣ No Unauthorized Self-Promotion**\nDo not share server invite links or advertise streams without staff permission."
)

ANNOUNCEMENT_TEXT = (
    "🎉 **WELCOME TO THE COMMUNITY SERVER!** 🎉\n\n"
    "👉 Step 1: Read rules in **#📑 | guidelines**\n"
    "👉 Step 2: Select your game roles in **#🏷️ | get_roles**\n"
    "👉 Step 3: Chat in **#💎 | general_chat**\n"
    "👉 Step 4: Need support? Open a ticket in **#🎯 | support_feedback**!"
)

class AutoSetupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="build_server", description="AUTOMATICALLY builds the exact Dynamo Gaming style layout (Categories, Channels, VC, Roles)!")
    @app_commands.checks.has_permissions(administrator=True)
    async def build_server_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild

        # 1. Create Roles & Hierarchy
        role_colors = {
            "TEAM HYDRA": discord.Color.dark_red(),
            "★═★ MOD / SUPPORT ★═★": discord.Color.red(),
            "Youtube Squad": discord.Color.green(),
            "Honorable citizen": discord.Color.gold(),
            "LEVEL 20": discord.Color.purple(),
            "LEVEL 15": discord.Color.magenta(),
            "LEVEL 10": discord.Color.blue(),
            "Gamers": discord.Color.blurple(),
            "Valorant": discord.Color.red(),
            "Rocket League": discord.Color.orange(),
            "BGMI": discord.Color.dark_green(),
            "CS:GO": discord.Color.dark_orange(),
            "Apex Legends": discord.Color.dark_magenta(),
            "Minecraft": discord.Color.green(),
            "Music Enthusiast": discord.Color.dark_teal(),
            "Meme Lord": discord.Color.teal()
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

        # 2. CATEGORY 1: WELCOME AREA
        cat_welcome = await guild.create_category("✦─────⦅ WELCOME AREA ⦆─────✦")
        c_guide = await create_tc(cat_welcome, "📑-|-guidelines", "📑 Official community rules and guidelines.")
        c_tour = await create_tc(cat_welcome, "📌-|-home_tour", "📌 Server overview and navigation tour.")
        c_roles = await create_tc(cat_welcome, "🏷️-|-get_roles", "🏷️ Select your game roles and playstyle!")

        embed_guide = discord.Embed(
            title="📜 COMMUNITY GUIDELINES & RULES",
            description=GUIDELINES_TEXT,
            color=discord.Color.blue()
        )
        await c_guide.send(embed=embed_guide)

        embed_roles = discord.Embed(
            title="🎮 GAMER ROLES & INTERESTS",
            description="Select your game and playstyle roles from the dropdown menus below!",
            color=discord.Color.blurple()
        )
        await c_roles.send(embed=embed_roles, view=CategoryRolesView())

        # 3. CATEGORY 2: LIVE SECTION
        cat_live = await guild.create_category("✦─────⦅ LIVE SECTION ⦆─────✦")
        await create_tc(cat_live, "🎗️-|-custom_info", "🎗️ Info on upcoming custom matches & scrims.")
        await create_vc(cat_live, "🔒 Live Stream")
        await create_vc(cat_live, "🔊 Waiting Lobby", limit=10)

        # 4. CATEGORY 3: IMPORTANT
        cat_important = await guild.create_category("✦─────⦅ IMPORTANT ⦆─────✦")
        c_announce = await create_tc(cat_important, "📢-|-announcement", "📢 Server updates and announcements.")
        await create_tc(cat_important, "📢-|-dynamo_live", "🔴 Live stream alerts and video uploads.")
        await create_tc(cat_important, "🎗️-|-rewards_giveaway", "🎁 Server giveaways and rewards.")
        await create_tc(cat_important, "🎗️-|-about_dynamo", "⭐ About the channel & creator.")

        embed_announce = discord.Embed(
            title="📢 WELCOME TO THE SERVER!",
            description=ANNOUNCEMENT_TEXT,
            color=discord.Color.gold()
        )
        await c_announce.send(embed=embed_announce)

        # 5. CATEGORY 4: SOCIAL HUB
        cat_social = await guild.create_category("✦─────⦅ SOCIAL HUB ⦆─────✦")
        await create_tc(cat_social, "💎-|-general_chat", "💬 Main text hangout channel.")
        await create_tc(cat_social, "🧩-|-thoughts", "💭 Share your thoughts and discussions.")
        await create_tc(cat_social, "📺-|-media_share", "📺 Share game highlights and videos.")
        await create_tc(cat_social, "🤡-|-memes", "🤡 Memes and funny gaming clips.")
        await create_tc(cat_social, "🖼️-|-museum", "🖼️ Server history and cool art.")
        await create_tc(cat_social, "📸-|-flashback", "📸 Screenshots and memories.")
        await create_vc(cat_social, "🔊 LOBBY - I", limit=30)
        await create_vc(cat_social, "🔊 LOBBY - II", limit=40)
        await create_vc(cat_social, "🔒 STAFF VC")

        # 6. CATEGORY 5: GAMES & RANKS
        cat_games = await guild.create_category("✦─────⦅ GAMES & RANKS ⦆─────✦")
        await create_tc(cat_games, "🪩-|-bot_commands", "🤖 Use bot commands here.")
        await create_tc(cat_games, "🍥-|-owo_world", "🍥 Anime & mini-games chat.")

        # 7. CATEGORY 6: CONTACT US
        cat_contact = await guild.create_category("✦─────⦅ CONTACT US ⦆─────✦")
        c_support = await create_tc(cat_contact, "🎯-|-support_feedback", "🎯 Support and help tickets.")
        await create_tc(cat_contact, "📑-|-complaints", "📑 Submit complaints or report rule breakers.")

        embed_support = discord.Embed(
            title="🎯 COMMUNITY SUPPORT & TICKETS",
            description="Click **📩 Open Support Ticket** below to contact moderators privately.",
            color=discord.Color.gold()
        )
        await c_support.send(embed=embed_support, view=TicketCreateView())

        # 8. CATEGORY 7: MUSIC LOUNGE
        cat_music = await guild.create_category("✦─────⦅ MUSIC LOUNGE ⦆─────✦")
        await create_tc(cat_music, "📌-|-music_cmnd", "🎶 Queue songs and manage music commands.")
        await create_vc(cat_music, "🎧 Jockie M{!}")
        await create_vc(cat_music, "🎧 HADE M{!}")

        # 9. CATEGORY 8: PLAY ZONE
        cat_play = await guild.create_category("✦─────⦅ PLAY ZONE ⦆─────✦")
        await create_tc(cat_play, "🤝-|-looking_for_squad", "👥 Find squadmates! Use /lfg command.")
        await create_vc(cat_play, "🔊 DUO - ❶", limit=2)
        await create_vc(cat_play, "🔊 SQUAD - ❶", limit=4)
        await create_vc(cat_play, "🔊 SQUAD - ❷", limit=4)

        # 10. CATEGORY 9: DISCONNECTED
        cat_afk = await guild.create_category("✦─────⦅ DISCONNECTED ⦆─────✦")
        await create_vc(cat_afk, "🔊 AFK")

        await interaction.followup.send(
            "🚀 **EXACT 'DYNAMO GAMING' LAYOUT BUILT SUCCESSFULLY!** 9 Categories, 25 Text & Voice Channels, Roles, and Interactive Panels installed!",
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoSetupCog(bot))
