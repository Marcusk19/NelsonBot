import pythonbible as KJB
import random
from discord.ext import commands

class Bible(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bible-verse', help='fetches a random bible verse')
    async def bible_verse(self, ctx):
        book = KJB.Book(random.randint(1, 66))
        numChapters = KJB.get_number_of_chapters(book)
        selectedChapter = random.randint(1, numChapters)
        numVerses = KJB.get_max_number_of_verses(book, selectedChapter)
        selectedVerse = random.randint(1, numVerses)
        verseID = KJB.get_verse_id(book, selectedChapter, selectedVerse)
        output = "From the book of " + str(book.title) + " Chapter " + str(selectedChapter) +  " Verse " +  str(selectedVerse) + ":\n" + KJB.get_verse_text(verseID)
        await ctx.send("```" + output + "```")


