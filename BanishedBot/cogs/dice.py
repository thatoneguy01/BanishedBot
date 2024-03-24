import discord
from discord.ext import commands
from discord import app_commands

import random

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class DiceNumberException(Exception):
        pass
    
    class DiceFacesException(Exception):
        pass
    
    class UnsupportedRollException(Exception):
        pass
    
    def roll_dice(number, sides):
        if number == "":
            number = 1
        try:
            number = int(number)
        except:
            raise Dice.DiceNumberException()
        if sides != 'f':
            try:
                sides = int(sides)
            except:
                raise Dice.DiceFacesException()
            return [random.randint(1,sides) for _ in range(number)]
        else:
            return [random.randint(-1,1) for _ in range(number)]

    #TODO: Expand roll syntax to include more of what roll20 does
    @commands.command(aliases=['r'], with_app_command=True)
    @app_commands.guilds(discord.Object(id=144252831833128960))
    async def roll(self, ctx, *, args):
        command = "".join(args).lower()
        command = command.replace('+', " + ").replace('-', " - ")
        rolls = command.split(" ")
        total = 0
        out = []
        isNeg = False
        try:
            for r in rolls:
                if r == '':
                    continue
                elif r == '+':
                    out.append(r)
                elif r =='-':
                    isNeg = True
                    out.append(r)
                elif r.isdigit():
                    total += int(r) * (-1 if isNeg else 1)
                    isNeg = False
                    out.append(r)
                else:
                    number, sides = r.split('d')
                    result = Dice.roll_dice(number, sides)
                    out.append(str(result))
                    total += sum(result) * (-1 if isNeg else 1)
        except Dice.DiceNumberException:
            await ctx.send("There was an error with your formula. Please fix the number of dice and try again.")
            return
        except Dice.DiceFacesException:
            await ctx.send("There was an error with your formula. Please fix the number/type of faces and try again.")
            return
        except:
            await ctx.send("There was an error with your formula. Please try again.")
            return
        await ctx.send(f"`{' '.join(out)}`\n## {total}")

async def setup(bot) -> None:
    await bot.add_cog(Dice(bot))