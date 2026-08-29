import discord
import aiohttp
import random
from discord.ext import commands, tasks
from discord import app_commands

SUBREDDITS = [
    "gamingmemes",
    "dankmemes",
    "memes",
    "wholesomememes",
    "VALORANT",
    "RocketLeague",
    "PUBGMobile"
]

class MemesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.auto_meme_channel_id = None

    async def fetch_meme(self, subreddit: str = None):
        if not subreddit:
            subreddit = random.choice(SUBREDDITS)

        url = f"https://meme-api.com/gimme/{subreddit}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if not data.get("nsfw", False):
                            return data
        except Exception:
            pass

        # Fallback API
        fallback_url = f"https://reddit.com/r/{subreddit}/random.json"
        headers = {"User-Agent": "VeldoraDiscordBot/1.0"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(fallback_url, headers=headers, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        post = data[0]["data"]["children"][0]["data"]
                        return {
                            "title": post.get("title", "Meme"),
                            "url": post.get("url", ""),
                            "postLink": f"https://reddit.com{post.get('permalink', '')}",
                            "subreddit": subreddit,
                            "ups": post.get("ups", 0),
                            "author": post.get("author", "Reddit User")
                        }
        except Exception:
            return None

        return None

    @commands.command(name="meme")
    async def meme_prefix(self, ctx: commands.Context, subreddit: str = None):
        """Fetch and post a random meme from Reddit."""
        async with ctx.typing():
            meme_data = await self.fetch_meme(subreddit)
            if not meme_data:
                await ctx.send("❌ Could not fetch a meme right now. Try again in a moment!")
                return

            embed = discord.Embed(
                title=meme_data.get("title", "Fresh Meme"),
                url=meme_data.get("postLink", ""),
                color=discord.Color.gold()
            )
            embed.set_image(url=meme_data.get("url"))
            embed.set_footer(text=f"👍 {meme_data.get('ups', 0)} | Subreddit: r/{meme_data.get('subreddit')} | Author: u/{meme_data.get('author')}")
            await ctx.send(embed=embed)

    @app_commands.command(name="meme", description="Fetch a fresh meme from Reddit (Gaming, Dank, or custom subreddit)")
    @app_commands.describe(category="Optional category or subreddit (e.g. gamingmemes, valorant, dankmemes)")
    async def meme_slash(self, interaction: discord.Interaction, category: str = None):
        await interaction.response.defer()
        meme_data = await self.fetch_meme(category)
        if not meme_data:
            await interaction.followup.send("❌ Could not fetch a meme right now. Try again in a moment!")
            return

        embed = discord.Embed(
            title=meme_data.get("title", "Fresh Meme"),
            url=meme_data.get("postLink", ""),
            color=discord.Color.gold()
        )
        embed.set_image(url=meme_data.get("url"))
        embed.set_footer(text=f"👍 {meme_data.get('ups', 0)} | Subreddit: r/{meme_data.get('subreddit')} | Author: u/{meme_data.get('author')}")
        await interaction.followup.send(embed=embed)

    @commands.command(name="set_automeme")
    @commands.has_permissions(administrator=True)
    async def set_automeme(self, ctx: commands.Context):
        """Sets the current channel for automatic meme posting every 2 hours."""
        self.auto_meme_channel_id = ctx.channel.id
        if not self.auto_meme_loop.is_running():
            self.auto_meme_loop.start()
        await ctx.send(f"✅ Auto-meme channel set to {ctx.channel.mention}! Memes will be posted automatically every 2 hours.")

    @tasks.loop(hours=2)
    async def auto_meme_loop(self):
        if self.auto_meme_channel_id:
            channel = self.bot.get_channel(self.auto_meme_channel_id)
            if channel:
                meme_data = await self.fetch_meme()
                if meme_data:
                    embed = discord.Embed(
                        title=meme_data.get("title", "Fresh Auto Meme"),
                        url=meme_data.get("postLink", ""),
                        color=discord.Color.gold()
                    )
                    embed.set_image(url=meme_data.get("url"))
                    embed.set_footer(text=f"👍 {meme_data.get('ups', 0)} | r/{meme_data.get('subreddit')} | Auto Meme")
                    await channel.send(embed=embed)

    @auto_meme_loop.before_loop
    async def before_auto_meme(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(MemesCog(bot))
