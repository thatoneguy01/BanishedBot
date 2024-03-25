from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Context, MemberConverter
from discord import User, app_commands
import discord

from BanishedBot.database.models.account import Account
from BanishedBot.utils import LockingCache

import time


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.accounts = LockingCache()
        self.voice_time = LockingCache()
        self.sync_cache.start()

    async def cog_load(self):
        async with self.accounts:
            db_accounts = await Account.get_all()
            for acc in db_accounts:
                self.accounts.cache[acc.username] = acc.balance
        return await super().cog_load()

    async def cog_unload(self) -> None:
        await self.sync_cache()
        return await super().cog_unload()
    
    async def mod_points(self, username, amount):
        async with self.accounts:
            try:
                self.accounts.cache[username] += amount
            except KeyError:
                self.accounts.cache[username] = amount
                

    @tasks.loop(minutes=5)
    async def sync_cache(self):
        print("SYNC CACHE")
        async with self.accounts:
            db_accounts = await Account.get_all()
            for acc in db_accounts:
                if acc.username in self.accounts.cache:
                    await acc.update(self.accounts.cache[acc.username])
                else:
                    self.accounts.cache[acc.username] = acc.balance
            db_names = [a.username for a in db_accounts]
            for (username, balance) in self.accounts.cache.items():
                if username not in db_names:
                    await Account.create(username, balance)
            
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(self.bot.command_prefix):
            return
        await self.mod_points(message.author.global_name, 1)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        async with self.voice_time:
            if ((not before.channel or before.channel.name != "General")
                and (after.channel and after.channel.name == "General")):
                self.voice_time.cache[member.global_name] = int(time.time())
                return
            if ((before.channel and before.channel.name == "General")
                and (not after.channel or after.channel.name != "General")):
                await self.mod_points(member.global_name, 
                                    (int(time.time())-self.voice_time.cache[member.global_name])/60)
                del(self.voice_time.cache[member.global_name])
                return
        
    @commands.hybrid_command(name="give", with_app_command=True)
    @app_commands.guilds(discord.Object(id=144252831833128960))
    async def give(self, context: Context, recipient: MemberConverter, amount: int):
        await self.mod_points(context.author.global_name, -amount)
        await self.mod_points(recipient.global_name, amount)
        await context.reply(f"{context.author.mention} gave {recipient.mention} {amount} points")

    @commands.hybrid_command(name="balance", with_app_command=True)
    @app_commands.guilds(discord.Object(id=144252831833128960))
    async def balance(self, context: Context):
        async with self.accounts:
            try:
                points = self.accounts.cache[context.author.global_name]
                s = "" if points == 1 else "s"
                await context.reply(f"You have {points} point{s}.")
            except KeyError:
                await self.mod_points(context.author.global_name, 0)
                await context.reply(f"You have 0 points.")

async def setup(bot) -> None:
    await bot.add_cog(Economy(bot))