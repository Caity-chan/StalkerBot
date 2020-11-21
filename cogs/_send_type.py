import discord
from discord.ext import commands

class send_type(commands.Converter):

  async def convert(self, ctx, value):
    # This function accepts channeltypes of 'c' and 'u'
    if value[0].lower() == 'c' or value[0].lower() == 'u':
      return value

    # It didn't convert and return an argument, so we've gotta raise an error
    raise commands.BadArgument("`{0}` isn't c or u.".format(value))    