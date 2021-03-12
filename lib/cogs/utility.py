import discord
import asyncio
from datetime import *
from discord.ext.commands import Cog
from discord.ext.commands import *
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
from discord.ext import tasks
from lib.bot.__init__ import bcolors
from lib.bot.__init__ import print_info
from lib.bot.__init__ import print_spec
from lib.bot.__init__ import print_spec
from lib.bot.__init__ import print_scheduler
from lib.bot.__init__ import print_cog


class Utility(Cog):
    def __init__(self, bot):
        self.bot = bot

    # THE REMINDER COMMAND. Specify when you want to be reminded, and the bot will ping you on that time.
    @commands.cooldown(2, 150, commands.BucketType.user)  # Cooldown of 1 use every 150 seconds per user.
    @command(name="remind", aliases=["reminder, remindme"], help="This command allows you to set a remind from 5 minutes to 7 days! Specify your value like 5m for 5 minutes.")
    async def remind(self, ctx, time, *, reminder):
        # print(time)
        # print(reminder)
        user = "<@!" + str(ctx.author.id) + ">"
        embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
        embed.set_footer(text="Requested by: " + "<@!" + str(ctx.author.id) + ">", icon_url=f"{ctx.message.author.avatar_url}")
        seconds = 0
        if reminder is None:
            embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.')  # Error message
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} day(s)"  # TODO: If the result is 1 then send as day otherwise as days.
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hour(s)"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minute(s)"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} second(s)"
        if seconds == 0:
            embed.add_field(name='Invalid Duration!',
                            value='Please specify a proper duration, `?!remind <time> <name>`. For example, `?!remind 5m Coding` for a reminder in 5 seconds.')
        elif seconds < 300:
            embed.add_field(name='Duration Too Small!',
                            value='You have specified a too short duration!\nThe minimum duration is 5 seconds.')
        elif seconds > 604800:
            embed.add_field(name='Duration Too Large!', value='You have specified too long of a duration!\nThe maximum duration is 7 days.')
        else:
            await ctx.reply(f"Alright, I will remind you about {reminder} in {counter}.")
            await asyncio.sleep(seconds)
            await ctx.send(f"Hey {user}, you asked me to remind you about {reminder} {counter} ago.")
            return
        await ctx.send(embed=embed)  # Send the embed with the information.

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("utility")

            # We can comment this out later if wanted.
            print(print_cog + print_spec + "Utility " + bcolors.ENDC + "cog started!")


def setup(bot):  # Define the cog
    bot.add_cog(Utility(bot))  # Add the cog to the main class (Utility).