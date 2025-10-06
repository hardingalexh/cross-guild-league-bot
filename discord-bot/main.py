import discord
from discord.ext import commands
from user_sync import UserSync
from react_listener import ReactListener

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
        for emoji in guild.emojis:
            print(f"  - {emoji} (name: {emoji.name})")
    print("------")

    # await bot.add_cog(UserSync(bot))
    await bot.add_cog(ReactListener(bot))
    print("Added cogs")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


bot.run(APP_TOKEN)
