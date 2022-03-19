from discord.ext.commands import Cog, command, Context
from discord.ext.commands import Bot

class ParrotCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="start")
    async def startParrot(self, ctx: Context):
        voice = ctx.author.voice

        if voice is None:
            await ctx.send("Looks like you're not in a voice channel")
            return
        
        await voice.channel.connect()