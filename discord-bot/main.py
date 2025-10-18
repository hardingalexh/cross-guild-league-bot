import discord
from discord.ext import commands
from user_sync import UserSync
from react_listener import ReactListener
import requests

## TODO: THIS ALL GOES IN AN ENV FILE
APP_TOKEN = "MTQyMTk3Mjk0Nzk1Nzk3NzE4Mw.Gb_j5t.GJHvyCFBrcr8rFAuBMv_qKkdGeGKfSgNM_84ms"
CHANNEL_NAME = "cross-guild-bot-test"


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix=">", intents=intents)


@bot.event
async def on_ready():
    # Note that async cogs hijacks STDIOut, so print statements may not appear in the console.
    await bot.add_cog(UserSync(bot))
    await bot.add_cog(ReactListener(bot))


@bot.command()
async def achievements(ctx):
    achievements = requests.get("http://localhost:8000/achievements").json()
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
    users = requests.get("http://localhost:8000/leaderboard").json()
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
