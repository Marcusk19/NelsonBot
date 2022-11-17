# TODO
import os
from discord.ext import commands
import re
import urllib.request, urllib.error, urllib.parse

class Scraper(commands.Cog):
    
    def __init__(self, bot):
        self.enableDownloads = False
        self.bot = bot
        self.path = os.getenv('DOWNLOAD_PATH')
        self.urlregex = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)')

    # Set a path for downloads
    # @commands.command(name='setpath', help='set path for downloads')
    # async def setpath(self, ctx, *, path):
    #     self.path = path
    #     await ctx.send("Download path updated to: `" + self.path + "`")
    # @setpath.error
    # async def setpath_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send('Please specify a path')

    # @commands.command(name='getpath', help='get path for downloads')
    # async def getpath(self, ctx):
    #     await ctx.send("Download path is: `" + self.path + "`")
    
    @commands.command(name='enabledownload', help='enable downloads for link detection')
    async def enabledownload(self, ctx):
        self.enableDownloads = False
        await ctx.send("Downloads are not permitted")

    @commands.command(name='disabledownload', help='disable downloads for link detection')
    async def disabledownload(self, ctx):
        self.enableDownloads = False
        await ctx.send("Disabled downloads")

    @commands.Cog.listener("on_message")
    async def find_link(self, message):
        if message.author == self.bot.user:
            return
        url = self.urlregex.search(message.content)
        if url is not None:
            
            if self.enableDownloads:
                filename = str(url.group(2)[1:-1]).replace("/", "_")

                try:
                    response = urllib.request.urlopen(str(url.group()))
                    webContent = response.read()
                    fullpath = str(self.path) + "/" + str(filename) + ".html"
                    
                    with open(fullpath, "wb") as fp:
                        fp.write(webContent)
                    print("Downloaded " + fullpath)

                    await message.channel.send("I've noticed you put a url in the chat! \n" +
                    "HTML file downloaded from: `" + url.group() + "`\n" +
                    "As " + filename + ".html")  
                except urllib.error.URLError as e:
                    print("Unable to download page: " + str(e.reason))
                    await message.channel.send("There was an error - see logs")
            
            pinned = await message.channel.pins()
            for pin in pinned:
                pin_url = self.urlregex.search(pin.content)
                if pin_url.group() == url.group():
                    print("matching url not pinned")
                    return
            await message.pin()
            await message.add_reaction("📌")
      
            
        
