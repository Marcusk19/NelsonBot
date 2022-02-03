from tokenize import String
import discord
from discord.ext import commands

def get_notes():
    f = open("src/notes.txt", "r")
    data = f.read()
    f.close()
    return data

class Butler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', help='purges text channel of messages')
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
    
    @commands.command(name='notes', help='displays patch notes')
    async def notes(self, ctx):
        output = get_notes()
        await ctx.send("```" + str(output) + "```")