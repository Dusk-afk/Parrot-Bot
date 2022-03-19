from services.client import Client
from services.parrot_cog import ParrotCog

TOKEN = "OTU0MzIzODA0NDUxMTMxNDQy.YjRdTQ.ulgvK66fa1xFjF_5Tt390Ceptaw"

bot = Client(
    command_prefix='$'
)

bot.add_cog(ParrotCog(bot))

# run the bot
bot.run(TOKEN)