import discord
from discord.ext import commands

## TODO: THIS ALL GOES IN AN ENV FILE
APP_TOKEN = ""
CHANNEL_NAME = "general"


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents)


@bot.command()
async def ping(ctx):
    channels = bot.get_all_channels()
    print(channels)
    await ctx.send("pong")


bot.run(APP_TOKEN)
