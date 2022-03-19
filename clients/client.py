from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.member import VoiceState, Member
from discord.channel import VoiceChannel
import asyncio

class Client(commands.Bot):

    FFMPEG_PATH = "ffmpeg.exe"

    async def on_ready(self):
        print(f"Running as {self.user.name} #{self.user.discriminator}")
    
    async def on_voice_state_update(self, member: Member, before: VoiceClient, after: VoiceClient):
        try:
            for i in range(len(self.voice_clients)):
                vc:VoiceClient = self.voice_clients[i]
            
                if vc.channel == after.channel:
                    await self._play_connect_sound(vc, member)
                
                if before.channel == vc.channel:
                    await self._play_disconnect_sound(vc, member)
        
        except Exception as e:
            print(f"Error: {e} | Voice Clients: {len(self.voice_clients)}")
    
    async def _play_connect_sound(self, channel: VoiceClient, member: Member):
        if channel.is_playing():
            channel.stop()
        channel.play(FFmpegPCMAudio(executable=self.FFMPEG_PATH, source='sounds/connected.mp3'))

    async def _play_disconnect_sound(self, channel: VoiceClient, member: Member):
        if channel.is_playing():
            channel.stop()
        channel.play(FFmpegPCMAudio(executable=self.FFMPEG_PATH, source='sounds/disconnected.mp3'))