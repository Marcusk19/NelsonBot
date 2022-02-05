import pandas as finPull
import random
from yahoo_fin import stock_info as tick
from discord.ext import commands, tasks
import os


class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = os.getenv('CHANNEL_ID')
        self.get_stocks.start()

    @tasks.loop(hours = 24)
    async def get_stocks(self):
        channel = self.bot.get_channel(int(self.channel_id))

        sp500tickers = finPull.DataFrame(tick.tickers_sp500())
        nasdaqtickers = finPull.DataFrame(tick.tickers_nasdaq())
        dowtickers = finPull.DataFrame(tick.tickers_dow())

        spList = sp500tickers[0].values.tolist()
        nasdaqList = nasdaqtickers[0].values.tolist()
        dowList = dowtickers[0].values.tolist()

        fullList = spList + nasdaqList + dowList

        badLetters = ['W', 'R', 'P', 'Q']

        for ticker in fullList:
            if len(ticker) > 4 and ticker[-1] in badLetters:
                fullList.remove(ticker)

        nelsonOracleLens = random.randint(0, len(fullList)-1)

        await channel.send("@here - the daily stock Nelson reccomends 📈 " + fullList[nelsonOracleLens]) 

    @get_stocks.before_loop
    async def before_get_stocks(self):
        await self.bot.wait_until_ready()
        