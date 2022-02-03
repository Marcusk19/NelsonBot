import asyncio
import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='joins a voice channel')
    async def join(self, ctx):
        await ctx.send("*Joining...*")
        channel = ctx.author.voice.channel
        # print(str(channel))
        await channel.connect()

    @commands.command(name='play', help='plays audio from yt link')
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        print(str(url))
        voice = ctx.voice_client
        info = ytdl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(URL, **ffmpeg_options)
        voice.play(source)
        await ctx.send('**Now playing:** {}'.format(info['title']))
        print("done")

    @commands.command(name='pause', help='pause playback')
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused ⏸️")
    
    @commands.command(name='resume', help='resume playback')
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Resumed ▶️")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @join.before_invoke
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Ruh roh you aren't connected to a voice channel")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()






