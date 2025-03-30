import discord
import discord.ext.commands
from pathlib import Path
import os

from core.settings import settings


async def load_cogs(bot: discord.ext.commands.Bot):
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{Path(file).stem}")
                print(f"Loaded cog: {file}")
            except Exception as e:
                print(f"Failed to load {file}: {e}")

    print("Slash commands synced.")

class Client(discord.ext.commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await load_cogs(self)
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message: discord.Message):
        print(f'Message received: {message.content}')
        await self.process_commands(message)

bot = Client()
bot.run(settings.TOKEN)