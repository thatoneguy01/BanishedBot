from discord.ext import commands
from discord.guild import Guild
from discord import ScheduledEvent

from BanishedBot.database.models.event import Event

from typing import Callable, Coroutine, Any
from datetime import datetime, timezone


class Time(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # TODO: why so slow?
    @commands.hybrid_command(name="timeuntil")
    async def time_until(self, ctx: commands.Context, *, arg):
        args = arg.split(" ")
        if args[0] == "add":
            op = args[0]
            try:
                time = datetime.fromisoformat(args[1]).astimezone(timezone.utc)
            except:
                await ctx.send("Event date must be in ISO format: 2000-01-01T00:00:00")
                return
            name = " ".join(args[2:])
        elif args[0] == "remove":
            op = args[0]
            name = " ".join(args[1:])
        else:
            op = None
            name = " ".join(args)
        guild = ctx.guild
        event: ScheduledEvent = await self.guild_event_by_name(guild, name)
        if event:
            if op:
                await ctx.send(
                    f"Cannot {op} an event with the same name as a server event"
                )
                return
            time_until = event.start_time - datetime.now(tz=timezone.utc)
            await ctx.send(str(time_until))
            return
        if op == "add":
            await Event.create(name, time)
            await ctx.send("Added event")
            return
        event: Event = await Event.event_by_name(name)
        if event:
            if op == "remove":
                await Event.remove(name)
                await ctx.send("Removed event")
            else:
                time_until = event.start_time.replace(
                    tzinfo=timezone.utc
                ) - datetime.now(tz=timezone.utc)
                await ctx.send(str(time_until))
            return
        await ctx.send(f"No event with name: {name}")

    async def guild_event_by_name(self, guild: Guild, name: str) -> ScheduledEvent:
        # Callable[[Any, Guild, str], Coroutine[Any, Any, ScheduledEvent]]:
        events = await guild.fetch_scheduled_events()
        for event in events:
            if event.name == name:
                return event
        return None


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Time(bot))
