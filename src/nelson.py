# bot.py
import os
import random
import discord
from discord import user
from discord.ext.commands.errors import CommandNotFound
from discord.ext import tasks
from dotenv import load_dotenv

import reddit

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
# client = discord.Client()
rh = reddit.RedditHandler("ncsu")

class FunStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Nelson has connected to Discord!')

# eight ball question event handler
    @commands.command(name='ask', help='Responds to yes or no question')
    async def eightball(self, ctx):
        eightball_responses = [
            'Yes',
            'No',
            'Definitely',
            'Absolutely Not',
            'Ask me later',
        ]  
        response = random.choice(eightball_responses)
        await ctx.send(response)

    @eightball.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You need to ask a question first')

    @commands.command(name='roll_dice', help='Generates random number 1-6')
    async def roll(self, ctx):
        await ctx.send(random.choice(range(1,6)))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("I don't know that command :(")

bot.add_cog(FunStuff(bot))
# client.run(TOKEN)
bot.run(TOKEN)