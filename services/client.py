from discord import FFmpegPCMAudio
from discord.guild import Guild
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.member import VoiceState, Member
from discord.channel import VoiceChannel
from services.audio_service import AudioService

from services.db import Db

class Client(commands.Bot):
    SPECIAL_ACCOUNTS = [484369293358923788, 520697243955757059]

    async def on_ready(self):
        print(f"Running as {self.user.name} #{self.user.discriminator}")
    
    async def on_voice_state_update(self, member: Member, before: VoiceClient, after: VoiceClient):
        try:
            for i in range(len(self.voice_clients)):
                vc:VoiceClient = self.voice_clients[i]
            
                if vc.channel == after.channel and before.channel != after.channel:
                    await self._play_connect_sound(vc, member)
                
                if before.channel == vc.channel and before.channel != after.channel:
                    await self._play_disconnect_sound(vc, member)
        
        except Exception as e:
            print(f"Error: {e} | Voice Clients: {len(self.voice_clients)}")
    
    async def _play_connect_sound(self, channel: VoiceClient, member: Member):
        if channel.is_playing():
            channel.stop()

        AudioService.play_tts_guild(channel, f'{member.display_name} {self.getConnectedText(member, channel.guild.id)}', channel.guild.id)

    async def _play_disconnect_sound(self, channel: VoiceClient, member: Member):
        if channel.is_playing():
            channel.stop()

        AudioService.play_tts_guild(channel, f'{member.display_name} {self.getDisonnectedText(member, channel.guild.id)}', channel.guild.id)
    
    def getLanguage(self, guild_id: int):
        return Db().of(guild_id).get_language()
        
    def getConnectedText(self, member: Member, guild_id: int):
        lang = self.getLanguage(guild_id)
        if member.id in self.SPECIAL_ACCOUNTS:
            return "sahab आ चुके है"
        
        if lang == "hi":
            return "आ चुके है"
        
        elif lang == "en":
            return "joined"
        
    def getDisonnectedText(self, member: Member, guild_id: int):
        lang = self.getLanguage(guild_id)
        if member.id in self.SPECIAL_ACCOUNTS:
            return "sahab जा चुके है"
        
        if lang == "hi":
            return "जा चुके है"
        
        elif lang == "en":
            return "left"

    async def on_guild_join(self, guild: Guild):
        Db().add_guild(guild.id)