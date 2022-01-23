# bot.py
import os
import random
import discord
from discord import user
from discord.ext.commands.errors import CommandNotFound
from discord.ext import tasks
from dotenv import load_dotenv

import reddit
import copypasta
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
        self.channel_id = os.getenv('CHANNEL_ID')
    
    @commands.Cog.listener("on_ready")
    async def ready(self):
        print('Nelson has connected to Discord!')
        self.get_new_post.start()

    @tasks.loop(hours=24)
    async def get_new_post(self):
        channel = self.bot.get_channel(int(self.channel_id))
        # print(str(channel))
        posts = rh.getTopFive()
        subreddit = posts[0].subreddit
        await channel.send("Top 5 Posts from r/" + str(subreddit))
        for post in posts:
            await channel.send(str(post.title))
            await channel.send(str(post.url))
            await channel.send("Score: " + str(post.score))
            await channel.send("=========================")


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
    
    @commands.command(name='ping', help='Test bot connection')
    async def ping_back(self, ctx):
        await ctx.send("ping ⊂(￣▽￣)⊃")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("I don't know that command (ಡ‸ಡ)")

# I went crazy on these listener messages

    @commands.Cog.listener("on_message")
    async def admin_rights(self, message):
        if message.author == self.bot.user:
            return
        if "admin" in message.content:
            await message.channel.send(copypasta.admin_talk)
    
    @commands.Cog.listener("on_message")
    async def jg_diff(self, message):
        if message.author == self.bot.user:
            return
        if "jg diff" in message.content:
            await message.channel.send(copypasta.jg_diff)

    @commands.Cog.listener("on_message")
    async def nft_steals(self, message):
        if message.author == self.bot.user:
            return
        if "screenshot" in message.content and "nft" in message.content:
            await message.channel.send(copypasta.nft_stealing)
    
    @commands.Cog.listener("on_message")
    async def hecker(self, message):
        if message.author == self.bot.user:
            return
        if "hack" in message.content and "nelson" in message.content:
            await message.channel.send(f'Hey {message.author}, {copypasta.hecker}')

    @commands.Cog.listener("on_message")
    async def bad_meme(self, message):
        if message.author == self.bot.user:
            return
        if "meme" in message.content:
            await message.channel.send(copypasta.bad_meme)

    @commands.Cog.listener("on_message")
    async def based_reaction(self, message):
        if message.author == self.bot.user:
            return
        lower_message = message.content.lower()
        if "based" in lower_message:
            await message.channel.send(copypasta.based_reaction)

    @commands.Cog.listener("on_message")
    async def periodt_purr(self, message):
        if message.author == self.bot.user:
            return
        if "periodt" in message.content or "purr" in message.content:
            await message.channel.send(copypasta.periodt_purr)
    
    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        await ctx.send(f'Hi {member.name}, welcome to the server! (´• ω •`)ﾉ')

bot.add_cog(FunStuff(bot))
bot.run(TOKEN)