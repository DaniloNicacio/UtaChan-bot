import discord
from discord import app_commands
from discord.ext import commands

class Channel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="hello", description="Says hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Channel(bot))
