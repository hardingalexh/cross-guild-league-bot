from discord.ext import tasks, commands
import requests


class UserSync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sync.start()

    def cog_unload(self):
        self.sync.cancel()

    async def upsert_user(self, user):
        print(user.display_avatar)
        payload = {
            "id": str(user.id),
            "name": user.name,
            "nick": user.nick,
            "discord_avatar_url": str(user.display_avatar.url) or None,
        }
        print(payload)
        ## TODO: handle failure
        r = requests.post("http://localhost:8000/user/upsert", json=payload)

    @tasks.loop(seconds=5.0)
    async def sync(self):
        """Finds all users with a given role and upserts them to the database"""
        for guild in self.bot.guilds:
            print(f"Guild: {guild.name} (id: {guild.id})")
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
                if users_with_role:
                    print(f"Users with role '{member_role.name}':")
                for user in users_with_role:
                    print(user.display_avatar.url, user.name, user.nick)
                    await self.upsert_user(user)

    @sync.before_loop
    async def before_sync(self):
        print("Waiting until bot is ready...")
        await self.bot.wait_until_ready()
