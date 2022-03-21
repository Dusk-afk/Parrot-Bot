from services.client import Client
from services.parrot_cog import ParrotCog

TOKEN = "OTU0MzIzODA0NDUxMTMxNDQy.YjRdTQ.m6NpYHcj_32T0YqVyYNGU-etgMM"

bot = Client(
    command_prefix='$'
)

bot.add_cog(ParrotCog(bot))

# run the bot
bot.run(TOKEN)