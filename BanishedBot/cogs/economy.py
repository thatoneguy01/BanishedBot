from discord.ext import commands
from discord.ext import tasks

from BanishedBot.database.objects.account import Account
from BanishedBot.database import Session

import time


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.account_cache = {}
        self.voice_time = {}

    async def cog_load(self):
        async with Session() as db:
            for acc in db.query(Account):
                self.account_cache[acc.username] = acc.balance
            await db.commit()
        return await super().cog_load()
    
    async def mod_points(self, username, amount):
        if username in self.account_cache:
            self.account_cache[username] = amount
        else:
            self.account_cache[username] += amount

    @tasks.loop(minutes=5)
    async def update_cache(self):
        async with Session() as db:
            for acc in db.query(Account):
                if acc.username in self.account_cache:
                    acc.balance = self.account_cache[acc.username]
                else:
                    self.account_cache[acc.username] = acc.balance
            await db.commit()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        await self.mod_points(message.author.global_name, 1)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if ((not before.channel or before.channel.name != "General")
            and (after.channel and after.channel.name == "General")):
            self.voice_time[member.global_name] = int(time.time())
            return
        if ((before.channel and before.channel.name == "General")
            and (not after.channel or after.channel.name != "General")):
            await self.mod_points(member.global_name, 
                                  (int(time.time())-self.voice_time[member.global_name])/60)
            del(self.mod_points[member.global_name])
            return

async def setup(bot) -> None:
    await bot.add_cog(Economy(bot))