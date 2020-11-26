from discord.ext import commands

import re

class SendSnowflake(commands.Converter):

  async def convert(self, ctx, value):
    
    # This function accepts any ints, and only returns a value if the int matches the format of a user or channel ID
    if re.match(r"^([0-9]){16,24}$", value):
      return value

    # It didn't convert and return an argument, so we've gotta raise an error
    raise commands.BadArgument("`{0}` isn't a valid ID.".format(value))    