from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Context, MemberConverter
from discord import Embed, app_commands, Interaction, ButtonStyle, User
from discord.ui import Button, View, button
import discord

from BanishedBot.database.models.trivia import Trivia as TriviaQuestion
from BanishedBot.cogs.economy import Economy

from typing import List
import random, asyncio, datetime

TEST_JSON = {"category": "film_and_tv", "id": "622a1c3d7cc59eab6f951c57", "correctAnswer": "Jingle All The Way", "incorrectAnswers": ["The Santa Claus", "I'll Be Home For Christmas", "Jack Frost"], "question": {"text": "In which 1996 Christmas film does Arnold Schwarzenegger play a father trying to get the must have toy for his son?"}, "tags": ["christmas", "film", "film_and_tv"], "difficulty": "hard"}
TEST_TRIVIA = TriviaQuestion.from_json(TEST_JSON)

class Trivia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.trivia_question:TriviaQuestion = TEST_TRIVIA
        super().__init__()

    async def cog_load(self) -> None:
        self.trivia_question = await TriviaQuestion.get_current()
        return await super().cog_load()
    
    @tasks.loop(time=datetime.time(hour=3))
    async def get_question(self):
        self.trivia_question = await TriviaQuestion.get_unused_or_reset()
    
    @commands.hybrid_command(name="trivia", with_app_command=True)
    @app_commands.guilds(discord.Object(id=144252831833128960))
    async def trivia(self, ctx: commands.Context):
        order = [0, 1, 2, 3]
        random.shuffle(order)
        view = TriviaView(self, self.trivia_question, order)
        embed = self.make_embed(order)
        await ctx.send(embed=embed, view=view)

    def make_embed(self, order: List) -> Embed:
        embed = Embed()
        embed.title = f'Trivia Question for {datetime.date.today().strftime("%B %d, %Y")}\nCategory: {self.trivia_question.category.replace("_", " ")}\nDifficulty: {self.trivia_question.difficulty}'
        embed.description = self.trivia_question.question
        labels = ["A", "B", "C", "D"]
        for i in range(4):
             embed.add_field(name="\u200B", value=f"{labels[i]}) {self.trivia_question.all_answers[order[i]]}", inline=False)
           
        return embed

    @commands.command()
    async def test_embed(self, ctx: commands.Context):
        await ctx.send(embed=self.make_embed())

    async def answered_correct(self, user: User) -> None:
        economy: Economy = self.bot.get_cog("Economy")
        await economy.mod_points(user.global_name, 100)
        dm_user = await self.bot.fetch_user(user.id)
        await dm_user.send("You have answered today's trivia correctly!  You have been awarded 100 points!")
        await self.update_stats(user, True)
    
    async def answered_incorrect(self, user: User) -> None:
        dm_user = await self.bot.fetch_user(user.id)
        await dm_user.send("You have answered today's trivia incorrectly.  Try again tomorrow.")
        await self.update_stats(user, False)

    async def update_stats(self, user: User, correct: bool) -> None:
        # TODO: implement
        pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load_questions(self, ctx: commands.Context):
        await TriviaQuestion.load_initial()


class TriviaView(View):
        def __init__(self, cog: Trivia, trivia_question: TriviaQuestion, order: List):
            super().__init__()
            self.cog = cog
            self.trivia_question = trivia_question
            self.answered: List = []
            self.answered_lock: asyncio.Lock = asyncio.Lock()
            self.add_buttons(order)

        def add_buttons(self, order: List) -> None:
            labels = ["A", "B", "C", "D"]
            for i in range(4):
                self.add_item(TriviaButton(self.trivia_question.all_answers[order[i]], label=labels[i]))


class TriviaButton(Button['TriviaView']):
    def __init__(self, answer, *, style: discord.ButtonStyle = ButtonStyle.grey, label: str = None):
        super().__init__(style=style, label=label)
        self.answer = answer

    async def callback(self, interaction: Interaction) -> None:
        assert self.view is not None
        view: TriviaView = self.view
        answered = False
        async with view.answered_lock:
            if interaction.user.global_name in view.answered:
                answered = True
            else:
                view.answered.append(interaction.user.global_name)
        if not answered:
            if self.answer == view.trivia_question.correct_answer:
                await view.cog.answered_correct(interaction.user)
            else:
                await view.cog.answered_incorrect(interaction.user)
        else:
            dm_user = await view.cog.bot.fetch_user(interaction.user.id)
            await dm_user.send("You have already answered today's question")
        await interaction.response.defer()
        #return await super().callback(interaction)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Trivia(bot))