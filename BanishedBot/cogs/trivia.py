from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Context, MemberConverter
from discord import User, app_commands, Interaction, ButtonStyle
from discord.ui import Button, View, button
import discord

from BanishedBot.database.models.trivia import Trivia as TriviaQuestion

import time, asyncio

class TriviaView(View):
        def __init__(self, cog, trivia_question):
            super().__init__()
            self.cog = cog
            self.trivia_question = trivia_question
            self.answered = []
            self.answered_lock = asyncio.Lock()

        def add_buttons(self):
            for answer in self.trivia_question.answers:
                self.add_item(TriviaButton(label=answer))


class TriviaButton(Button['TriviaView']):
    def __init__(self, *, style: discord.ButtonStyle = ButtonStyle.grey, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | discord.Emoji | discord.PartialEmoji | None = None, row: int | None = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: TriviaView = self.view
        answered = False
        async with view.answered_lock:
            if interaction.user.global_name in view.answered:
                answered = True
            else:
                view.answered.append(interaction.user.global_name)
        if not answered:
            if self.label == view.trivia_question.correct_answer:
                await view.cog.answered_correct(interaction.user.global_name)
            else:
                await view.cog.answered_incorrect(interaction.user.global_name)
        return await super().callback(interaction)
    

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trivia_date = None
        self.trivia_question = None
        super().__init__()

    async def cog_load(self) -> None:
        return await super().cog_load()

    async def answered_correct(self, member: MemberConverter):
        economy = self.bot.get_cog("Economy")
        await economy.mod_points(member.global_name, 100)
        await member.send("You have answered today's trivia correctly!  You have been awarded 100 points!")
        await self.update_stats(member, True)
    
    async def answered_incorrect(self, member: MemberConverter):
        await member.send("You have answered today's trivia incorrectly.  Try again tomorrow.")
        await self.update_stats(member, False)

    async def update_stats(self, member, correct):
        # TODO: implement
        pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load_questions(self, ctx):
        await TriviaQuestion.load_initial()


async def setup(bot) -> None:
    await bot.add_cog(Trivia(bot))