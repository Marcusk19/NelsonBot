# bot.py
import os
import random
import discord
from discord import user
from discord.ext.commands.errors import CommandNotFound
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# eight ball question event handler
@bot.command(name='ask', help='Responds to yes or no question')
async def eightball(ctx, question):
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
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You need to ask a question first')

@bot.command(name='roll_dice', help='Generates random number 1-6')
async def roll(ctx):
    await ctx.send(random.choice(range(1,6)))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('Your command was not found :(')


bot.run(TOKEN)