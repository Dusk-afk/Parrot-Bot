import asyncio
from discord.ext.commands import Cog, command, Context
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

class ParrotCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="start")
    async def start(self, ctx: Context):
        voice = ctx.author.voice

        if voice is None:
            await ctx.send("Looks like you're not in a voice channel")
            return
        
        try:
            await voice.channel.connect()
        
        except:
            await ctx.send("Looks like I'm already in a voice channel.\nIf not then try again after a minute.")
            # for i in range(len(self.bot.voice_clients)):
            #     vc:VoiceClient = self.bot.voice_clients[i]
            #     if vc.guild.id == ctx.guild.id:
            #         await vc.disconnect()
            #         await asyncio.sleep(1)
            #         await voice.channel.connect()
    
    @command(name="ping")
    async def ping(self, ctx: Context):
        await ctx.send(f"Ping: {round(self.bot.latency, 2)}ms")
    
    @command(name="sing")
    async def sing(self, ctx: Context):
        await ctx.send("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you")

    
    @command(name="stop")
    async def stop(self, ctx: Context):
        try:
            await ctx.voice_client.disconnect()
        except Exception as e:
            print(e)