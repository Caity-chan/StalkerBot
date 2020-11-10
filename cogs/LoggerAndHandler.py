import discord
from discord.ext import commands

import aiohttp
import io


class LoggerAndHandler(commands.Cog, name="Logger And Handler"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Sends the name and membercount of every server the bot joins"""

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url('https://discordapp.com/api/webhooks/744353242322043001/V3WMdShI8L8LZLStNUBaqG2WI-qZrdofCQFM1QkW4oLTIcRA4TMC5ffKFpS2JyIXp96w', adapter=discord.AsyncWebhookAdapter(session))
            await webhook.send(f'StalkerBot was added to `{guild.name}` (`{guild.id}`). `{len([i for i in guild.members if not i.bot])}` members.', username='On Guild Join Event')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Sends the name and membercount of every server the bot leaves"""

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url('https://discordapp.com/api/webhooks/744353242322043001/V3WMdShI8L8LZLStNUBaqG2WI-qZrdofCQFM1QkW4oLTIcRA4TMC5ffKFpS2JyIXp96w', adapter=discord.AsyncWebhookAdapter(session))
            await webhook.send(f'StalkerBot was removed from `{guild.name}` (`{guild.id}`). `{len([i for i in guild.members if not i.bot])}` members.', username='On Guild Leave Event')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Sends all errors to a logging channel with a webhook"""

        codeblock_error = f"```py\n{error}```"

        # Channel Sending
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.TooManyArguments):
            return await ctx.send(codeblock_error)
        elif isinstance(error, (commands.BadArgument, commands.BadUnionArgument)):
            return await ctx.send(codeblock_error)
        #elif isinstance(error, commands.MissingRequiredArgument):
            #return await ctx.send(codeblock_error)
        elif isinstance(error, commands.NotOwner):
            return await ctx.send(codeblock_error)
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.author.send(codeblock_error)
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.author.send(codeblock_error)

        # Webhook Sending
        embed = discord.Embed()
        embed.color = 0xFF000000
        embed.title = ctx.message.content
        embed.set_footer(text=f"Author: {str(ctx.author)} ({ctx.author.id})\nChannel: {ctx.channel.name} ({ctx.channel.id})\nGuild: {ctx.guild.name} ({ctx.guild.id})")
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url('https://discordapp.com/api/webhooks/744353242322043001/V3WMdShI8L8LZLStNUBaqG2WI-qZrdofCQFM1QkW4oLTIcRA4TMC5ffKFpS2JyIXp96w', adapter=discord.AsyncWebhookAdapter(session))
            if len(str(error)) >= 1970:
                data = io.StringIO(str(error))
                data.seek(0)
                await webhook.send(file=discord.File(data, filename="error.py"))
            else:
                embed.description = error
                await webhook.send(embed=embed)
                #await webhook.send(f"```py\n{error}```\n`{str(ctx.author)}`(`{ctx.author.id}`)\n`{ctx.message.content}`")

        # And raise error again so it goes to the console as a full traceback
        raise error

    @commands.command(aliases=['countservers'])
    @commands.is_owner()
    async def countguilds(self, ctx):
        """Counts how many guilds have the bot"""

        await ctx.send(f"The bot is in `{len(self.bot.guilds)}` guilds.")

    @commands.command()
    @commands.is_owner()
    async def countusers(self, ctx):
        """Counts how many unique user IDs there are"""

        async with self.bot.database() as db:
            distinctRows = await db("SELECT DISTINCT userid FROM keywords;")
            rows = await db("SELECT * FROM keywords;")

        await ctx.send(f"`{len(distinctRows)}` unique users have set up keywords and there are `{len(rows)}` keywords in total.")


def setup(bot):
    bot.add_cog(LoggerAndHandler(bot))
