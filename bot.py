from services.client import Client
from services.db import Db
from services.parrot_cog import ParrotCog

TOKEN = "OTU0MzIzODA0NDUxMTMxNDQy.GY1145.vSpktJRAef2-unRFdQI4UzmcK8H1mwwq3RhRX4"

Db()
bot = Client(
    command_prefix='$'
)

bot.add_cog(ParrotCog(bot))

# run the bot
bot.run(TOKEN)
