import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio',
    'noplaylist': 'True',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    'preferredcodec': 'mp3',
    'preferredquality': '192'
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
        voice = ctx.voice_client # obtain voice channel
        info = ytdl.extract_info(url, download=False) # use ytdl to extract source for playback
        URL = info['formats'][0]['url'] # hmmmm this is probably url formatting
        source = await discord.FFmpegOpusAudio.from_probe(URL, **ffmpeg_options) # use discord.FFmpegOpusAudio to make source (I think)
        voice.play(source)
        # print information about what is playing
        await ctx.send('**Now playing:** {}'.format(info['title']) +  " - " + ctx.author.display_name)
        await ctx.message.delete()
        print("done")

    @commands.command(name='pause', help='pause playback')
    async def pause(self, ctx):
        await ctx.voice_client.pause()
    
    @commands.command(name='resume', help='resume playback')
    async def resume(self, ctx):
        await ctx.voice_client.resume()

    @commands.command(name='stop', help='stops playback and disconnects from voice')
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

    # check user calling the command is in a voice chananel before running /join or /play
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






