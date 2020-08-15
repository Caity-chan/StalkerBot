import discord
from discord.ext import commands
import asyncpg
import json


class FilterCommands(commands.Cog, name = "Filter Commands"):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def filter(self, ctx, filterType, filter = None):
        """Sets a filter provided a type (can be "list" which lists all your filters)"""

        pass

    @filter.command()
    async def text(self, ctx, filter):
        """Adds a text filter"""

        connection = await asyncpg.connect(**self.bot.database_auth)
        await connection.fetch("INSERT INTO filters (userid, textfilter) VALUES($1, $2);", ctx.author.id, filter)
        await connection.close()
        await ctx.send(f"Added `{filter}` to your text filter list")

    @filter.command()
    @commands.guild_only()
    async def channel(self, ctx, filter:discord.TextChannel):
        """Adds a channel filter"""

        connection = await asyncpg.connect(**self.bot.database_auth)
        await connection.fetch("INSERT INTO filters (userid, channelfilter) VALUES($1, $2);", ctx.author.id, filter)
        await connection.close()
        await ctx.send(f"Added {filter.mention} to your channel filter list")
                
    @filter.command(name="list")
    async def _list(self, ctx):
        """Lists all your filters"""

        connection = await asyncpg.connect(**self.bot.database_auth)
        rows = await connection.fetch("select * from filters where userid = $1;", ctx.author.id)
        await connection.close()

        if len(rows) == 0:
            await ctx.send(f"You don't have any keywords. Set some up by running the `{ctx.prefix}addkeyword` command")
            return

        textFilters = []
        channelFilters = []
        
        x = 0
        while x != len(rows):
            if rows[x]['textfilter'] is not None:
                textFilters.append(rows[x]['textfilter'])
            x = x + 1
        textFilters = ', '.join(textFilters)

        x = 0
        while x != len(rows):
            if rows[x]['channelfilter'] is not None:
                channelFilters.append(rows[x]['channelfilter'])
            x = x + 1
        channelFilters = ', '.join(channelFilters)

        await ctx.send(f"Text Filters: `{textFilters}` \n Channel Filters: `{channelFilters}`")


    @filter.group()
    async def remove(self, ctx):
        """Removes a filter (text or channel)"""
        pass

    @remove.command(name="text")
    async def _text(self, ctx, filter):
        """Removes a text filter"""

        
        connection = await asyncpg.connect(**self.bot.database_auth)
        await connection.fetch("DELETE FROM filters WHERE userid=$1 and textfilter=$2;", ctx.author.id, filter)
        await connection.close()

    @remove.command(name="channel")
    @commands.guild_only()
    async def _channel(self, ctx, filter:discord.TextChannel):
        """Removes a channel filter"""

        connection = await asyncpg.connect(**self.bot.database_auth)
        await connection.fetch("DELETE FROM filters WHERE userid=$1 and textfilter=$2;", ctx.author.id, filter)
        await connection.close()



def setup(bot):
    bot.add_cog(FilterCommands(bot))
