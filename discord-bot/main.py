import discord
from discord.ext import commands
from ears import Ears

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
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
    await bot.add_cog(Ears(bot))


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


bot.run(APP_TOKEN)
