import asyncio
import sys

import discord
import discord.ext.commands
from pathlib import Path
import os

from core.settings import settings


sys.path.append(str(Path(__file__).parent))

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
        intents.voice_states = True
        super().__init__(command_prefix="!", intents=intents)
        self.voice_check_tasks = {}

    async def setup_hook(self):
        await load_cogs(self)
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message: discord.Message):
        await self.process_commands(message)

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        voice_state = member.guild.voice_client
        if voice_state is None:
            return

        if len(voice_state.channel.members) == 1:
            await asyncio.sleep(300)
            await voice_state.disconnect()


bot = Client()
bot.run(settings.TOKEN)