import discord
from discord import app_commands, VoiceState, VoiceProtocol
from discord.ext import commands
from typing import List
import asyncio
from core.utils.yt_utils import get_audio_stream, get_video_url


class Player(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.current_song: str | None = None
        self.current_channel: any = None
        self.playlist: List[str] = []
        self.is_playing_flag: bool = False
        super().__init__()

    @app_commands.command(name="hello", description="Says hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")

    @app_commands.command(name="play", description="Play a song!")
    async def play(self, interaction: discord.Interaction, song: str):
        await interaction.response.defer()

        user: VoiceState | None = interaction.user.voice

        if user is None:
            await interaction.followup.send(
                f"{interaction.user.mention}, you need to connect to a voice channel."
            )
            return

        bot_voice: VoiceProtocol | None = interaction.guild.voice_client

        self.current_channel = interaction.channel

        if bot_voice:
            if bot_voice.channel != user.channel:
                await bot_voice.move_to(user.channel)
                await interaction.followup.send(f"Moved to {user.channel.name}.", ephemeral=True)
        else:
            bot_voice = await user.channel.connect()

        url = get_video_url(song)
        stream_url = get_audio_stream(url)
        self.playlist.append(stream_url)
        await interaction.followup.send(content=f"Added to queue: {stream_url['title']}")

        if not self.is_playing_flag:
            await self.play_next(interaction, bot_voice)


    async def play_next(self, interaction: discord.Interaction, voice_client: discord.VoiceClient):
        if len(self.playlist) == 0:
            self.current_song = None
            self.is_playing_flag = False
            if self.current_channel:
                await self.current_channel.send("There are no more songs in the queue")
            return

        stream_url = self.playlist.pop(0)
        self.current_song = stream_url['title']
        self.is_playing_flag = True

        if self.current_channel:
            await self.current_channel.send(f"Now playing: {self.current_song}")

        def after_playing(error):
            if error:
                print(f"Error in playback: {error}")

            asyncio.run_coroutine_threadsafe(self.play_next(interaction, voice_client), self.bot.loop)

        voice_client.play(
            discord.FFmpegOpusAudio(
                stream_url['stream_url'],
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            ),
            after=after_playing
        )

    @app_commands.command(name="stop", description="Clear the queue and stops the current song")
    async def stop(self, interaction: discord.Interaction):
        user: VoiceState | None = interaction.user.voice

        if user is None:
            await interaction.response.send_message(
                f"{interaction.user.mention} you need to connect to a voice channel")
            return

        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        if not voice_client:
            await interaction.response.send_message("I am not in a voice channel.")
            return

        await interaction.response.defer()

        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()
            self.current_song = None
            self.playlist.clear()
            self.is_playing_flag = False
            await interaction.followup.send("Stopped current song and cleared the queue.")
        else:
            await interaction.followup.send("There's no song currently playing.")

    @app_commands.command(name="resume", description="Resume the current song")
    async def resume(self, interaction: discord.Interaction):
        user: VoiceState | None = interaction.user.voice

        if user is None:
            await interaction.response.send_message(
                f"{interaction.user.mention} you need to connect to a voice channel.")
            return

        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        if not voice_client:
            await interaction.response.send_message("I am not in a voice channel.")
            return

        await interaction.response.defer()

        if voice_client.is_paused():
            voice_client.resume()
            await interaction.followup.send(f"Resuming {self.current_song}")
        else:
            await interaction.followup.send("There's no song currently paused.")

    @app_commands.command(name="pause", description="Pause the current song")
    async def pause(self, interaction: discord.Interaction):
        user: VoiceState | None = interaction.user.voice

        if user is None:
            await interaction.response.send_message(
                f"{interaction.user.mention} you need to connect to a voice channel.")
            return

        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        if not voice_client:
            await interaction.response.send_message("I am not in a voice channel.")
            return

        await interaction.response.defer()

        if voice_client.is_playing():
            voice_client.pause()
            await interaction.followup.send(f"Pausing {self.current_song}")
        else:
            await interaction.followup.send("There's no song currently playing.")

    @app_commands.command(name="leave", description="Clear current playlist and leaves the channel")
    async def leave(self, interaction: discord.Interaction):
        user: VoiceState | None = interaction.user.voice
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        await interaction.response.defer()

        if user is None:
            await interaction.followup.send(
                f"{interaction.user.mention} you need to connect to a voice channel.")
            return

        if not voice_client:
            await interaction.followup.send("I am not in a voice channel.")
            return

        self.current_song = None
        self.current_channel = None
        self.playlist.clear()
        self.is_playing_flag = False
        await voice_client.disconnect()
        await interaction.followup.send("Leaving the current channel.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Player(bot))
