import discord
from discord.ext import commands
from user_sync import UserSync
from react_listener import ReactListener
import requests
import os

## READ ENV VARIABLES
APP_TOKEN = os.getenv("APP_TOKEN", "")
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "cross-guild-bot-test")
API_URL = os.getenv("API_URL", "http://localhost:8000")

# ENABLE DISCORD INTENTS
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix=">", intents=intents)


## ADD COGS ON READY
@bot.event
async def on_ready():
    await bot.add_cog(UserSync(bot))
    await bot.add_cog(ReactListener(bot))


@bot.command()
async def achievements(ctx):
    """Sends a message to the channel summarizing all achievements and pre-populates reactions

    Args:
        ctx (_type_): Discord bot context
    """
    if ctx.channel.name != CHANNEL_NAME:
        return
    achievements = requests.get(f"{API_URL}/achievements").json()
    emojis = ctx.guild.emojis
    msg = "# Available Achievements:\n"
    for achievement in achievements:
        # find the emoji object in the guild by name
        emoji_obj = discord.utils.get(emojis, name=achievement["emoji"])
        msg += f"- {emoji_obj if emoji_obj else achievement['emoji']} - *{achievement['name']}*\n"
        msg += f"  - _{achievement['description']}_\n"
    msg_obj = await ctx.send(msg)
    for achievement in achievements:
        emoji_obj = discord.utils.get(emojis, name=achievement["emoji"])
        if emoji_obj:
            await msg_obj.add_reaction(emoji_obj)
        else:
            await msg_obj.add_reaction(achievement["emoji"])


@bot.command()
async def leaderboard(ctx):
    """Sends a message to the channel summarizing the current leaderboard"""

    if ctx.channel.name != CHANNEL_NAME:
        return
    users = requests.get(f"{API_URL}/leaderboard").json()
    msg = "# Leaderboard:\n"
    leaderboard = {}
    for user in users:
        berries = sum([a["achievement"]["bounty"] for a in user["achievement_links"]])
        leaderboard[user["name"]] = berries
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    for i, (username, berries) in enumerate(sorted_leaderboard):
        msg += f"{i + 1}. **{username}** - {berries:,} Berries\n"

    await ctx.send(msg)


bot.run(APP_TOKEN)
