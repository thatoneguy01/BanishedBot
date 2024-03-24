import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)

        await ctx.send(
            f"Synced {len(fmt)} commands to the current guild."
        )
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def global_sync(self, ctx):
        fmt = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(fmt)} commands to the current guild."
        )
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unsync(self, ctx):
        ctx.bot.tree.clear_commands(guild=ctx.guild)
        sync_tree = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(
            f"Unsynced {len(sync_tree)} commands to the current guild."
        )
        return
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def global_unsync(self, ctx):
        ctx.bot.tree.clear_commands(guild=None)
        sync_tree = await ctx.bot.tree.sync()
        await ctx.send(
            f"Unsynced {len(sync_tree)} commands to the current guild."
        )
        return

async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))