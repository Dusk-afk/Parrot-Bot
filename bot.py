from services.client import Client
from services.parrot_cog import ParrotCog

TOKEN = "OTU0MzIzODA0NDUxMTMxNDQy.YjRdTQ.AeaUfCYs7gj4qSZ3OWKDLt7Ui7w"

bot = Client(
    command_prefix='$'
)

bot.add_cog(ParrotCog(bot))

# run the bot
bot.run(TOKEN)