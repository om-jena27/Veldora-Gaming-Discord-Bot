import asyncio
import logging
import discord
from discord.ext import commands
from discord import app_commands
from cogs.roles import CategoryRolesView
from cogs.verify import VerifyView
from cogs.tickets import TicketCreateView

GUIDELINES_TEXT = (
    "Welcome to our Veldora Gaming Community! Please follow our server guidelines:\n\n"
    "**1️⃣ Be Respectful**\nNo toxic behavior, harassment, hate speech, or offensive language.\n\n"
    "**2️⃣ Voice Channel Rules**\nNo loud noise, mic spamming, or ear-rape audio. Respect squad channel user limits.\n\n"
    "**3️⃣ Fair Gaming & No Cheats**\nCheating, hacking, or exploiting in games is strictly prohibited.\n\n"
    "**4️⃣ Channel Usage**\nKeep discussions in relevant channels: memes in `#🤡｜memes`, bot commands in `#🪩｜bot_commands`.\n\n"
    "**5️⃣ No Unauthorized Self-Promotion**\nDo not share server invite links or advertise streams without staff permission."
)

ANNOUNCEMENT_TEXT = (
    "🎉 **WELCOME TO VELDORA GAMING COMMUNITY!** 🎉\n\n"
    "👉 Step 1: Read rules in **#📑｜guidelines**\n"
    "👉 Step 2: Select your game roles in **#🏷️｜get_roles**\n"
    "👉 Step 3: Chat in **#💎｜general_chat**\n"
    "👉 Step 4: Need support? Open a ticket in **#🎯｜support_feedback**!"
)

class AutoSetupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def execute_build_server(self, guild: discord.Guild):
        # 0. REMOVE OLD CHANNELS & CATEGORIES WITH RATE LIMIT PROTECTION
        logging.info("Deleting existing channels...")
        for channel in list(guild.channels):
            try:
                await channel.delete(reason="Resetting server layout")
                await asyncio.sleep(0.3)
            except Exception as e:
                logging.warning(f"Could not delete channel {channel.name}: {e}")

        # 1. CREATE ROLES
        logging.info("Creating roles...")
        role_colors = {
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
            "Event Notified": discord.Color.yellow()
        }

        created_roles = {}
        for role_name, color in role_colors.items():
            existing = discord.utils.get(guild.roles, name=role_name)
            if not existing:
                try:
                    created_roles[role_name] = await guild.create_role(name=role_name, color=color)
                    await asyncio.sleep(0.3)
                except Exception as e:
                    logging.warning(f"Could not create role {role_name}: {e}")
            else:
                created_roles[role_name] = existing

        # Helper functions with rate-limit pauses
        async def create_cat(name):
            try:
                cat = await guild.create_category(name)
                await asyncio.sleep(0.5)
                return cat
            except Exception as e:
                logging.error(f"Error creating category {name}: {e}")
                return None

        async def create_tc(category, name, topic=None):
            try:
                tc = await category.create_text_channel(name=name, topic=topic)
                await asyncio.sleep(0.5)
                return tc
            except Exception as e:
                logging.error(f"Error creating TC {name}: {e}")
                return None

        async def create_vc(category, name, limit=0):
            try:
                vc = await category.create_voice_channel(name=name, user_limit=limit)
                await asyncio.sleep(0.5)
                return vc
            except Exception as e:
                logging.error(f"Error creating VC {name}: {e}")
                return None

        # 2. CATEGORY 1: WELCOME AREA
        cat_welcome = await create_cat("✦─────⦅ WELCOME AREA ⦆─────✦")
        if cat_welcome:
            c_welcome = await create_tc(cat_welcome, "👋｜welcome", "👋 Welcome greetings for new community members!")
            c_guide = await create_tc(cat_welcome, "📑｜guidelines", "📑 Official community rules and guidelines.")
            c_tour = await create_tc(cat_welcome, "📌｜home_tour", "📌 Server overview and navigation tour.")
            c_roles = await create_tc(cat_welcome, "🏷️｜get_roles", "🏷️ Select your game roles and playstyle!")

            if c_guide:
                embed_guide = discord.Embed(
                    title="📜 COMMUNITY GUIDELINES & RULES",
                    description=GUIDELINES_TEXT,
                    color=discord.Color.blue()
                )
                await c_guide.send(embed=embed_guide)
                await asyncio.sleep(0.3)

            if c_roles:
                embed_roles = discord.Embed(
                    title="🎮 GAMER ROLES & INTERESTS",
                    description="Select your game and playstyle roles from the dropdown menus below!",
                    color=discord.Color.blurple()
                )
                await c_roles.send(embed=embed_roles, view=CategoryRolesView())
                await asyncio.sleep(0.3)

        # 3. CATEGORY 2: LIVE SECTION
        cat_live = await create_cat("✦─────⦅ LIVE SECTION ⦆─────✦")
        if cat_live:
            await create_tc(cat_live, "🎗️｜custom_info", "🎗️ Info on upcoming custom matches & scrims.")
            await create_vc(cat_live, "🔒 Live Stream")
            await create_vc(cat_live, "🔊 Waiting Lobby", limit=10)

        # 4. CATEGORY 3: IMPORTANT
        cat_important = await create_cat("✦─────⦅ IMPORTANT ⦆─────✦")
        if cat_important:
            c_announce = await create_tc(cat_important, "📢｜announcement", "📢 Server updates and announcements.")
            await create_tc(cat_important, "📢｜stream_alerts", "🔴 Live stream alerts and video uploads.")
            await create_tc(cat_important, "🎗️｜rewards_giveaway", "🎁 Server giveaways and rewards.")
            await create_tc(cat_important, "🎗️｜about_community", "⭐ About our gaming community.")

            if c_announce:
                embed_announce = discord.Embed(
                    title="📢 WELCOME TO THE SERVER!",
                    description=ANNOUNCEMENT_TEXT,
                    color=discord.Color.gold()
                )
                await c_announce.send(embed=embed_announce)
                await asyncio.sleep(0.3)

        # 5. CATEGORY 4: SOCIAL HUB
        cat_social = await create_cat("✦─────⦅ SOCIAL HUB ⦆─────✦")
        if cat_social:
            await create_tc(cat_social, "💎｜general_chat", "💬 Main text hangout channel.")
            await create_tc(cat_social, "🧩｜thoughts", "💭 Share your thoughts and discussions.")
            await create_tc(cat_social, "📺｜media_share", "📺 Share game highlights and videos.")
            await create_tc(cat_social, "🤡｜memes", "🤡 Memes and funny gaming clips.")
            await create_tc(cat_social, "🖼️｜museum", "🖼️ Server history and cool art.")
            await create_tc(cat_social, "📸｜flashback", "📸 Screenshots and memories.")
            await create_vc(cat_social, "🔊 LOBBY - I", limit=30)
            await create_vc(cat_social, "🔊 LOBBY - II", limit=40)
            await create_vc(cat_social, "🔒 STAFF VC")

        # 6. CATEGORY 5: GAMES & RANKS
        cat_games = await create_cat("✦─────⦅ GAMES & RANKS ⦆─────✦")
        if cat_games:
            await create_tc(cat_games, "🪩｜bot_commands", "🤖 Use bot commands here.")
            await create_tc(cat_games, "🍥｜owo_world", "🍥 Anime & mini-games chat.")

        # 7. CATEGORY 6: CONTACT US
        cat_contact = await create_cat("✦─────⦅ CONTACT US ⦆─────✦")
        if cat_contact:
            c_support = await create_tc(cat_contact, "🎯｜support_feedback", "🎯 Support and help tickets.")
            await create_tc(cat_contact, "📑｜complaints", "📑 Submit complaints or report rule breakers.")

            if c_support:
                embed_support = discord.Embed(
                    title="🎯 COMMUNITY SUPPORT & TICKETS",
                    description="Click **📩 Open Support Ticket** below to contact moderators privately.",
                    color=discord.Color.gold()
                )
                await c_support.send(embed=embed_support, view=TicketCreateView())
                await asyncio.sleep(0.3)

        # 8. CATEGORY 7: MUSIC LOUNGE
        cat_music = await create_cat("✦─────⦅ MUSIC LOUNGE ⦆─────✦")
        if cat_music:
            await create_tc(cat_music, "📌｜music_cmnd", "🎶 Queue songs and manage music commands.")
            await create_vc(cat_music, "🎧 Jockie M{!}")
            await create_vc(cat_music, "🎧 HADE M{!}")

        # 9. CATEGORY 8: PLAY ZONE
        cat_play = await create_cat("✦─────⦅ PLAY ZONE ⦆─────✦")
        if cat_play:
            await create_tc(cat_play, "🤝｜looking_for_squad", "👥 Find squadmates! Use /lfg command.")
            await create_vc(cat_play, "🔊 DUO - ❶", limit=2)
            await create_vc(cat_play, "🔊 SQUAD - ❶", limit=4)
            await create_vc(cat_play, "🔊 SQUAD - ❷", limit=4)

        # 10. CATEGORY 9: DISCONNECTED
        cat_afk = await create_cat("✦─────⦅ DISCONNECTED ⦆─────✦")
        if cat_afk:
            await create_vc(cat_afk, "🔊 AFK")

        logging.info("Server build completed successfully!")

    @app_commands.command(name="build_server", description="Removes old channels/categories and builds the complete fresh server layout!")
    @app_commands.checks.has_permissions(administrator=True)
    async def build_server_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await self.execute_build_server(interaction.guild)
        try:
            await interaction.followup.send("🚀 **SERVER RESET & COMPLETE LAYOUT BUILT SUCCESSFULLY!**", ephemeral=True)
        except Exception:
            pass

    @commands.command(name="build_server")
    @commands.has_permissions(administrator=True)
    async def build_server_prefix(self, ctx: commands.Context):
        """Prefix command: !build_server"""
        msg = await ctx.send("🧹 Resetting server and building full 9-category layout (please wait ~15s)...")
        await self.execute_build_server(ctx.guild)
        try:
            await msg.edit(content="🚀 **SERVER RESET & COMPLETE LAYOUT BUILT SUCCESSFULLY!** All 9 Categories and 26 Channels created!")
        except Exception:
            pass


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoSetupCog(bot))
