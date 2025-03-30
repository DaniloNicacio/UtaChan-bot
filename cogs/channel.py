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

        await interaction.response.defer()

        if bot_voice:
            if bot_voice.channel == user.channel:
                # Just a placeholder
                return

            await bot_voice.move_to(user.channel)
            await interaction.followup.send(f"Moved to {user.channel.name}.", ephemeral=True)
            return

        await user.channel.connect()
        await interaction.followup.send("Joined your channel.", ephemeral=True)

    @app_commands.command(name="stop", description="Clear the queue and leaves the channel")
    async def stop(self, interaction: discord.Interaction):
        user: VoiceState | None = interaction.user.voice

        if user is None:
            await interaction.response.send_message(
                f"{interaction.user.mention} you need to connect to a voice channel.")
            return

        bot_voice: VoiceProtocol | None = interaction.guild.voice_client

        await interaction.response.defer()

        if bot_voice:
            if bot_voice.channel == user.channel:
                await bot_voice.disconnect()
                return
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(Channel(bot))
