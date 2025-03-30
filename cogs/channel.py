import discord
from discord import app_commands, VoiceState, VoiceProtocol
from discord.ext import commands

class Channel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="hello", description="Says hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

    @app_commands.command(name="play", description="Play a song!")
    async def play(self, interaction: discord.Interaction):
        user: VoiceState | None = interaction.user.voice

        if user is None:
            await interaction.response.send_message(f"{interaction.user.mention} you need to connect to a voice channel.")
            return

        bot_voice: VoiceProtocol | None = interaction.guild.voice_client

        if bot_voice:
            if bot_voice.channel == user.channel:
                # Just a placeholder
                return

            await bot_voice.move_to(user.channel)
            return
        await user.channel.connect()
        await interaction.response.send_message("Joined your channel")

async def setup(bot: commands.Bot):
    await bot.add_cog(Channel(bot))
