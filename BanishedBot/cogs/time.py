from discord.ext import commands
from discord.guild import Guild

from BanishedBot.database.models.event import Event

from datetime import datetime, timezone

class Time(commands.Cog):

    @commands.hybrid_command(name="timeuntil")
    async def time_until(self, ctx: commands.Context, *args):
        if args[0] == 'add':
            op = args[0]
            try:
                time = datetime.fromisoformat(args[1]).astimezone(timezone.utc)
            except:
                ctx.send("Event date must be in ISO format: 2000-01-01T00:00:00")
                return
            name = ' '.join(args[2:])
        elif args[0] == "remove":
            op = args[0]
            name = ' '.join(args[1:])
        else:
            op = None
            name = ' '.join(args)
        guild = ctx.guild
        event = await self.guild_event_by_name(guild, name)
        if event:
            if op:
                ctx.send(f"Cannot {op} an event with the same name as a server event")
                return
            time_until = event.start_time - datetime.now(tz=timezone.utc)
            ctx.send(str(time_until))
            return    
        event = Event.event_by_name(name)
        if event:
            if op == "add":
                Event.create(name, time)
            elif op == "remove":
                Event.remove(name)
            else:
                time_until = event.start_time - datetime.now(tz=timezone.utc)
                ctx.send(str(time_until))
            return
        ctx.send(f"No event with name: {name}")


    async def guild_event_by_name(self, guild: Guild, name: str):
        events = await guild.fetch_scheduled_events()
        for event in events:
            if event.name == name:
                return event
        return None
        