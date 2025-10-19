from discord.ext import tasks, commands
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")


class UserSync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sync.start()

    def cog_unload(self):
        self.sync.cancel()

    async def upsert_user(self, user):
        payload = {
            "id": str(user.id),
            "name": user.name,
            "nick": user.nick,
            "discord_avatar_url": str(user.display_avatar.url) or None,
        }
        ## TODO: handle failure
        r = requests.post(f"{API_URL}/user/upsert", json=payload)

    @tasks.loop(seconds=5.0)
    async def sync(self):
        """Finds all users with a given role and upserts them to the database"""
        for guild in self.bot.guilds:
            ## get the role object for "League Member"
            member_role = next(
                (role for role in guild.roles if role.name.lower() == "league member"),
                None,
            )
            if member_role:
                ## get user objects with given role
                users_with_role = [
                    member for member in guild.members if member_role in member.roles
                ]
                for user in users_with_role:
                    await self.upsert_user(user)

    @sync.before_loop
    async def before_sync(self):
        print("Waiting until bot is ready...")
        await self.bot.wait_until_ready()
