# bot.py
import os, json
from dotenv import load_dotenv

import discord
from discord.ext import commands

from constant import SRC_DIR
import database

if not os.path.isfile("config.json"):
    print("No config file")
else:
    with open("config.json") as f:
        config = json.load(f)

class BanishedBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="?", intents=intents)
        self.database = None
        self.config = config
        self.loaded_cogs = []

    async def init_db(self):
        import database.objects
        async with database.engine.begin() as conn:
            await conn.run_sync(database.Base.metadata.create_all)
        session = database.Session()
        await session.commit()
        await session.close()

    async def load_cogs(self):
        for cog in self.config["loaded_cogs"]:
            await self.load_extension(f"cogs.{cog}")

    async def setup_hook(self):
        await self.init_db()
        self.database = database.Session()
        await self.load_cogs()
        #exit()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = BanishedBot()
bot.run(TOKEN)