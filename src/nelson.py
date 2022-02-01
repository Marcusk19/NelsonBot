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
startup = True

bot = commands.Bot(command_prefix='/')
# client = discord.Client()
rh = reddit.RedditHandler("ncsu")

class FunStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.channel_id = os.getenv('CHANNEL_ID')
    
    def get_new_post(self):
        output_str = ""
        posts = rh.getTopFive()
        subreddit = posts[0].subreddit
        output_str += "Top 5 Posts from r/" + str(subreddit)
        for post in posts:
            output_str = output_str + str(post.title) + "\n"
            output_str += str(post.url) + "\n"
            output_str += "Upvotes: " + str(post.score) + "\n"
            output_str += "============================\n"
        return output_str
    
    @commands.Cog.listener("on_ready")
    async def ready(self):
        print('Nelson has connected to Discord!')
        self.routine_posts.start()

    @tasks.loop(hours=24)
    async def routine_posts(self):
        channel = self.bot.get_channel(int(self.channel_id))
        # print(str(channel))
        output_str = self.get_new_post()
        if not startup:
            await channel.send(output_str)


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
        await ctx.send("ping 👋 😊")

    @commands.command(name='gettop', help='get top 5 posts')
    async def gettop(self, ctx):
        self.get_new_post()
        await ctx.send("check your posts channel 📮")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("I don't know that command (ಡ‸ಡ)")

# I went crazy on these listener messages

    @commands.Cog.listener("on_message")
    async def message_parse(self, message):
        if message.author == self.bot.user:
            return
        message_lower = message.content.lower()
        if "admin" in message_lower:
            await message.channel.send(copypasta.admin_talk)
        if "jg diff" in message_lower:
            await message.channel.send(copypasta.jg_diff)
        if "screenshot" in message_lower and "nft" in message_lower:
            await message.channel.send(copypasta.nft_stealing)
        if "hack" in message_lower and "nelson" in message_lower:
            await message.channel.send(f'Hey {message.author}, {copypasta.hecker}')
        if "meme" in message_lower:
            await message.channel.send(copypasta.bad_meme)
        if "based" in message_lower:
            await message.channel.send(copypasta.based_reaction)
        if "periodt" in message_lower or "purr" in message_lower:
            await message.channel.send(copypasta.periodt_purr)

    
    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        await ctx.send(f'Hi {member.name}, welcome to the server! (´• ω •`)ﾉ')
        
bot.add_cog(FunStuff(bot))
bot.run(TOKEN)
startup = False