import json
import glob
import os
import logging
import sys

import discord
from discord.ext import commands, tasks
import asyncpg


logging.basicConfig(stream=sys.stdout)
logging.getLogger("discord").setLevel(logging.INFO)
logger = logging.getLogger("stalkerbot")
logger.setLevel(logging.DEBUG)


with open("config.json") as a:
    config = json.load(a)


bot_token = config["token"]
database_auth = config["database"]


class DatabaseConnection(object):

    def __init__(self, conn=None):
        self.conn = conn

    @classmethod
    async def get_connection(cls):
        v = cls()
        await v.connect()
        return v

    async def connect(self):
        self.conn = await asyncpg.connect(**database_auth)

    async def disconnect(self):
        await self.conn.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.disconnect()

    async def __call__(self, sql, *args):
        return await self.conn.fetch(sql, *args)


async def get_prefix(bot, message):
    """Actually changes the prefix it looks for"""
    if message.guild is None:
        return commands.when_mentioned_or("s.")(bot,message)

    connection = await asyncpg.connect(**database_auth)
    prefixRows = await connection.fetch("SELECT * from prefix where guildid = $1", message.guild.id)
    await connection.close()

    try:
        prefix = prefixRows[0]['prefix']
    except IndexError:
        prefix = "s."
    return commands.when_mentioned_or(prefix)(bot,message)


intents = discord.Intents.default()
intents.members = True  # Damn you to heck Discord
intents.typing = False
intents.presences = False

bot = commands.AutoShardedBot(command_prefix=get_prefix, intents=intents)
bot.database_auth = database_auth
bot.database = DatabaseConnection
bot.logger = logger


@bot.event
async def on_ready():
    game = discord.Game(f"Currently down || Stalking {len(bot.guilds)} guilds.")
    await bot.change_presence(status=discord.Status.online, activity=game)
    change_presence_loop.start()


@tasks.loop(minutes=10)
async def change_presence_loop():
    game = discord.Game(f"Currently down || Stalking {len(bot.guilds)} guilds.")
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command()
@commands.is_owner()
async def reloadall(ctx):
    """Reloads all the cogs"""

    [bot.reload_extension(i[:-3].replace(os.sep, ".")) for i in glob.glob("cogs/*.py") if i[5] != "_"]
    await ctx.send("🔁 Reloaded all loadable cogs.")
    


[bot.load_extension(i[:-3].replace(os.sep, ".")) for i in glob.glob("cogs/*.py") if i[5] != "_"]
bot.load_extension("jishaku")
bot.run(bot_token)
