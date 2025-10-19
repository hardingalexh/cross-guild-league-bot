from discord.ext import commands
import json
import requests
import os

ROLE = os.getenv("USER_ROLE", "League Member")
CHANNEL = os.getenv("CHANNEL_NAME", "cross-guild-bot-test")
API_URL = os.getenv("API_URL", "http://localhost:8000")


class ReactListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("emojis.json", "r") as f:
            emojis = json.load(f)
            inv_emojis = {v: k for k, v in emojis.items()}
            self.emojis = inv_emojis

    async def handle_react(self, action, reaction, user):
        ## only in specific channel
        if reaction.message.channel.name != CHANNEL:
            return
        ## ignore reactions from the bot itself
        if user.id == self.bot.user.id:
            return
        ## only fro users with specific role
        if ROLE not in [role.name for role in user.roles]:
            return

        payload = {
            "id": str(user.id),
            "name": user.name,
            "nick": user.nick,
        }

        ## default emojis are str, custom are Emoji type
        if type(reaction.emoji) is str:
            # if reaction.emoji not in self.emojis:
            emoji = reaction.emoji
        else:
            emoji = reaction.emoji.name
        r = requests.post(
            f"{API_URL}/user/{action}_achievement?emoji={emoji}",
            json=payload,
        )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.handle_react("add", reaction, user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.handle_react("remove", reaction, user)
