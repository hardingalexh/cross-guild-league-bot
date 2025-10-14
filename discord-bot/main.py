import discord
from discord.ext import commands
from user_sync import UserSync
from react_listener import ReactListener
import requests

## TODO: THIS ALL GOES IN AN ENV FILE
APP_TOKEN = "MTQyMTk3Mjk0Nzk1Nzk3NzE4Mw.Gb_j5t.GJHvyCFBrcr8rFAuBMv_qKkdGeGKfSgNM_84ms"
CHANNEL_NAME = "general"


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
    msg = "Available Achievements:\n"
    for achievement in achievements:
        # find the emoji object in the guild by name
        emoji_obj = discord.utils.get(emojis, name=achievement["emoji"])
        msg += f"{emoji_obj if emoji_obj else achievement['emoji']} - {achievement['name']}\n"
    msg_obj = await ctx.send(msg)
    # for achievement in achievements:
    #     emoji_obj = discord.utils.get(emojis, name=achievement["emoji"])
    #     if emoji_obj:
    #         print("sending", emoji_obj)
    #         await msg_obj.add_reaction(emoji_obj)
    #         ## TODO: handle default emojis


@bot.command()
async def leaderboard(ctx):
    await ctx.send("Leaderboard command called")


bot.run(APP_TOKEN)
