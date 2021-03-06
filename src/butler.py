from tokenize import String
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord.utils import get

def get_notes():
    f = open("notes.txt", "r")
    data = f.read()
    f.close()
    return data

class Butler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = os.getenv('CHANNEL_ID')

    # @commands.command(name='clear', help='purges text channel of messages')
    # async def clear(self, ctx, amount=5):
    #     await ctx.channel.purge(limit=amount+1)
    #     await ctx.message.delete()
    
    @commands.command(name='info', help='displays patch notes')
    async def info(self, ctx):
        output = get_notes()
        await ctx.send("```" + str(output) + "```")

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member):
        print("user update detected")
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Hi {0.mention} welcome to the server!'.format(member))

    @commands.Cog.listener("on_user_update")
    async def on_user_update(self, before, after):
        print("user update detected")
        channel = after.guild.system_channel
        if channel is not None:
            await channel.send('Wow {0.mention} updated their profile check it out!'.format(before))
    
    @commands.command(name='joined', help='says when a member joined')
    async def joined(self, ctx, *, member: discord.Member):
        await ctx.send(f'**{member.display_name} joined on {member.joined_at}**')

    @joined.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("I need a member's name")

    @commands.Cog.listener("on_guild_emojis_update")
    async def on_guild_emojis_update(self, guild, before, after):
        channel = self.bot.get_channel(int(self.channel_id))
        await channel.send(f'emojis updated for {guild.name}')

    @commands.Cog.listener("on_guild_channel_create")
    async def on_guild_channel_create(self, created):
        channel = self.bot.get_channel(int(self.channel_id))
        await channel.send(f'new channel **{created.name}** created')
    
    @commands.Cog.listener("on_guild_channel_delete")
    async def on_guild_channel_delete(self, deleted):
        channel = self.bot.get_channel(int(self.channel_id))
        await channel.send(f'channel **{deleted.name}** was deleted')
    
    @commands.command(name='request', help='pings server admins for request (requires "Admin" role to exist)')
    async def request(self, ctx, *, request):
        admin = get(ctx.guild.roles, name='Admin')
        await ctx.send("^ " + admin.mention)
    @request.error
    async def request_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(ctx.author.display_name + ", please specify your ask")

    @commands.command(name='game', help='pings everyone with associated game role')
    async def game(self, ctx, *, role):
        role = get(ctx.guild.roles, name=role)
        if role is not None:
            await ctx.send(role.mention + " - " + ctx.author.display_name + " is looking for a game")
            await ctx.message.delete()
        else:
            await ctx.send("could not find that role")