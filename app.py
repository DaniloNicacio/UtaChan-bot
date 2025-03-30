from app.core.settings import settings
from app.main import Client

bot = Client()
bot.run(settings.TOKEN)