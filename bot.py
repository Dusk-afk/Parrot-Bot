import os
import dotenv

from services.client import Client
from services.db import Db
from services.parrot_cog import ParrotCog

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

Db()
bot = Client(
    command_prefix='$'
)

bot.add_cog(ParrotCog(bot))

bot.run(token)
