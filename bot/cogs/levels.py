import os
import math
import io
import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
import aiohttp

# In-memory XP storage (User_ID -> {"xp": int, "level": int, "messages": int})
user_xp_data = {}

def get_user_data(user_id: int):
    if user_id not in user_xp_data:
        user_xp_data[user_id] = {"xp": 0, "level": 1, "messages": 0}
    return user_xp_data[user_id]

def xp_for_level(level: int) -> int:
    return 100 * (level ** 2)

class LevelsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        user_id = message.author.id
        data = get_user_data(user_id)
        data["xp"] += 15
        data["messages"] += 1

        current_level = data["level"]
        needed_xp = xp_for_level(current_level)

        if data["xp"] >= needed_xp:
            data["level"] += 1
            new_level = data["level"]
            
            # Level Up announcement in channel
            try:
                embed = discord.Embed(
                    title="🎉 LEVEL UP!",
                    description=f"Congratulations {message.author.mention}! You just leveled up to **Level {new_level}**! 🚀",
                    color=discord.Color.gold()
                )
                embed.set_thumbnail(url=message.author.display_avatar.url)
                await message.channel.send(embed=embed)
            except Exception:
                pass

            # Auto-assign level roles if configured
            guild = message.guild
            level_roles = {
                5: "🥉 Level 5 - Rookie",
                15: "🥈 Level 15 - Veteran",
                30: "🥇 Level 30 - Elite",
                50: "👑 Level 50 - Legend"
            }
            if new_level in level_roles:
                role_name = level_roles[new_level]
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    try:
                        role = await guild.create_role(name=role_name, color=discord.Color.purple())
                    except Exception:
                        role = None
                if role and role not in message.author.roles:
                    try:
                        await message.author.add_roles(role)
                    except Exception:
                        pass

    async def generate_rank_card(self, member: discord.Member) -> discord.File:
        user_id = member.id
        data = get_user_data(user_id)
        level = data["level"]
        xp = data["xp"]
        prev_level_xp = xp_for_level(level - 1) if level > 1 else 0
        next_level_xp = xp_for_level(level)
        
        current_level_xp = xp - prev_level_xp
        required_level_xp = next_level_xp - prev_level_xp
        progress = min(max(current_level_xp / max(required_level_xp, 1), 0.0), 1.0)

        # Calculate rank position
        sorted_users = sorted(user_xp_data.items(), key=lambda x: x[1]["xp"], reverse=True)
        rank_pos = 1
        for idx, (uid, udata) in enumerate(sorted_users, 1):
            if uid == user_id:
                rank_pos = idx
                break

        # Load Template Image from bot/assets/
        assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        template_path = os.path.join(assets_dir, "rank template.png")

        if os.path.exists(template_path):
            base = Image.open(template_path).convert("RGBA")
        else:
            base = Image.new("RGBA", (900, 300), (20, 20, 35, 255))

        W, H = base.size
        draw = ImageDraw.Draw(base)

        # Fetch Avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(member.display_avatar.url) as resp:
                    if resp.status == 200:
                        avatar_data = await resp.read()
                        avatar_img = Image.open(io.BytesIO(avatar_data)).convert("RGBA")
        except Exception:
            avatar_img = None

        if avatar_img:
            avatar_size = (int(H * 0.45), int(H * 0.45))
            avatar_img = avatar_img.resize(avatar_size, Image.Resampling.LANCZOS)
            
            # Make avatar circular
            mask = Image.new("L", avatar_size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0) + avatar_size, fill=255)

            avatar_x = int(W * 0.05)
            avatar_y = int(H * 0.28)
            base.paste(avatar_img, (avatar_x, avatar_y), mask)

        # Fonts
        try:
            font_title = ImageFont.truetype("arial.ttf", int(H * 0.08))
            font_sub = ImageFont.truetype("arial.ttf", int(H * 0.05))
            font_small = ImageFont.truetype("arial.ttf", int(H * 0.04))
        except Exception:
            font_title = font_sub = font_small = ImageFont.load_default()

        # Draw Stats Text
        text_x = int(W * 0.30)
        text_name_y = int(H * 0.25)
        text_stats_y = int(H * 0.45)

        draw.text((text_x, text_name_y), f"{member.display_name}", fill=(255, 255, 255, 255), font=font_title)
        draw.text((text_x, text_stats_y), f"LEVEL {level}  •  RANK #{rank_pos}", fill=(0, 220, 255, 255), font=font_sub)
        draw.text((text_x, int(H * 0.60)), f"XP: {xp} / {next_level_xp}", fill=(200, 200, 220, 255), font=font_small)

        # Draw Progress Bar
        bar_x = text_x
        bar_y = int(H * 0.72)
        bar_w = int(W * 0.62)
        bar_h = int(H * 0.06)

        draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=(40, 40, 60, 200), outline=(80, 80, 110, 255))
        fill_w = int(bar_w * progress)
        if fill_w > 0:
            draw.rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], fill=(0, 220, 255, 255))

        # Save to buffer
        buf = io.BytesIO()
        base.save(buf, format="PNG")
        buf.seek(0)
        return discord.File(buf, filename="rank_card.png")

    @commands.command(name="rank")
    async def rank_prefix(self, ctx: commands.Context, member: discord.Member = None):
        """Prefix command: !rank"""
        target = member or ctx.author
        async with ctx.typing():
            card_file = await self.generate_rank_card(target)
            await ctx.send(file=card_file)

    @app_commands.command(name="rank", description="View your level, XP, server rank, and rank card!")
    @app_commands.describe(member="Member to view rank for (optional)")
    async def rank_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        await interaction.response.defer()
        card_file = await self.generate_rank_card(target)
        await interaction.followup.send(file=card_file)

    @commands.command(name="leaderboard")
    async def leaderboard_prefix(self, ctx: commands.Context):
        """Prefix command: !leaderboard"""
        sorted_users = sorted(user_xp_data.items(), key=lambda x: x[1]["xp"], reverse=True)[:10]
        
        embed = discord.Embed(
            title="🏆 VELDORA SERVER LEADERBOARD",
            description="Top active members ranked by XP & Level!",
            color=discord.Color.gold()
        )

        if not sorted_users:
            embed.description = "No rank data available yet! Start chatting to earn XP!"
        else:
            for idx, (uid, udata) in enumerate(sorted_users, 1):
                user = ctx.guild.get_member(uid)
                uname = user.display_name if user else f"User ID {uid}"
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
                embed.add_field(
                    name=f"{medal} {uname}",
                    value=f"Level `{udata['level']}` | XP `{udata['xp']}` | Messages `{udata['messages']}`",
                    inline=False
                )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(LevelsCog(bot))
