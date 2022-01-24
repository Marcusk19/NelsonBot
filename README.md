# NelsonBot # 
Discord bot in Python

## Installation ##
Clone this repo and then start the bot first building the docker image: <br />
`docker build -t nelson .`
Then you can run the container: <br />
`docker run -d nelson`

## Structure ##
All the code is located in `src` directory. <br />
You will need to create a .env file with your own tokens and credentials for Discord and Reddit APIs. <br />
Guides below for how to obtain your tokens: <br />
* [Discord Developer Portal](https://discord.com/developers/docs/topics/oauth2)
* [Reddit Developer Portal](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) <br />
You should copy the contents of `example.env` to your .env file and replace the values with your own: <br/>
`cp src/example.env .env` <br />

## External References ##
Docs for using discore.py and praw<br />
* [praw](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html)
* [discord.py](https://discordpy.readthedocs.io/en/stable/index.html)



