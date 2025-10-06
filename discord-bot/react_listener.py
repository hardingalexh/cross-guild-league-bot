from discord.ext import commands
import json
import requests


class ReactListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("emojis.json", "r") as f:
            emojis = json.load(f)
            inv_emojis = {v: k for k, v in emojis.items()}
            self.emojis = inv_emojis

    async def handle_react(self, action, reaction, user):
        ## only in specific channel
        if reaction.message.channel.name != "general":
            return
        ## only if message author is from the bot
        if reaction.message.author != self.bot.user:
            return
        payload = {
            "id": str(user.id),
            "name": user.name,
            "nick": user.nick,
        }
        ## default emojis are str, custom are Emoji type
        if type(reaction.emoji) is str:
            if reaction.emoji not in self.emojis:
                return
            emoji = self.emojis[reaction.emoji]
        else:
            emoji = reaction.emoji.name

        requests.post(
            f"http://localhost:8000/user/f{action}_achievement?emoji={emoji}",
            json=payload,
        )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        self.handle_react("add", reaction, user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        self.handle_react("remove", reaction, user)
