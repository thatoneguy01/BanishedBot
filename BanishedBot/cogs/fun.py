import discord
from discord import Message, Member
from discord.ext import commands
from discord.ext.commands import Context

import aiohttp


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.content.startswith(self.bot.command_prefix):
            return
        if not message.author.global_name:
            return
        torin = self.bot.get_user(156874457745457152)
        if message.author == torin:
            if "ould of" in message.content:
                pre = (
                    message.content[: message.content.find("ould of")]
                    .split(" ")[-1]
                    .capitalize()
                )
                message.reply(
                    f"HEY FUCKER, ITS {pre}OULD'VE, NOT {pre}OULD OF!!!  ITS NOT EVEN LESS LETTERS!!!"
                )

    @commands.hybrid_command(name="fact")
    async def fact(self, ctx: Context):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="joke")
    async def joke(self, ctx: Context):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com/") as request:
                if request.status == 200:
                    text = await request.text()
                    embed = discord.Embed(description=text, color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
