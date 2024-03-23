from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Context
from discord import User

from BanishedBot.database.objects.account import Account
from BanishedBot.database import Session
from BanishedBot.utils import LockingCache

import time


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.accounts = LockingCache()
        self.voice_time = LockingCache()

    async def cog_load(self):
        async with Session() as db, self.accounts as accounts:
            for acc in db.query(Account):
                accounts.cache[acc.username] = acc.balance
            await db.commit()
        return await super().cog_load()
    
    async def mod_points(self, username, amount):
        async with self.accounts as accounts:
            if username in accounts.cache:
                accounts.cache[username] = amount
            else:
                accounts.cache[username] += amount

    @tasks.loop(minutes=5)
    async def update_cache(self):
        async with Session() as db, self.accounts as accounts:
            for acc in db.query(Account):
                if acc.username in accounts.cache:
                    acc.balance = accounts.cache[acc.username]
                else:
                    accounts.cache[acc.username] = acc.balance
            await db.commit()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        await self.mod_points(message.author.global_name, 1)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        async with self.voice_time as voice_time:
            if ((not before.channel or before.channel.name != "General")
                and (after.channel and after.channel.name == "General")):
                voice_time[member.global_name] = int(time.time())
                return
            if ((before.channel and before.channel.name == "General")
                and (not after.channel or after.channel.name != "General")):
                await self.mod_points(member.global_name, 
                                    (int(time.time())-voice_time[member.global_name])/60)
                del(self.mod_points[member.global_name])
                return
        
    @commands.hybrid_command()
    async def give(self, context: Context, recipient: User, amount: int):
        async with self.accounts as accounts:
            accounts.cache[context.author.global_name] -= amount
            accounts.cache[recipient.global_name] += amount
            context.reply(f"{context.author.mention} gave {recipient.mention} {amount} points")

    @commands.hybrid_command()
    async def balance(self, context: Context):
        async with self.accounts as accounts:
            context.reply(f"You have {accounts.cache[context.author.global_name]} points.")

async def setup(bot) -> None:
    await bot.add_cog(Economy(bot))