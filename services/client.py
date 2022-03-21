import json
from discord import FFmpegPCMAudio
from discord.guild import Guild
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.member import VoiceState, Member
from discord.channel import VoiceChannel
from services.FFmpegPCMAudioGTTS import FFmpegPCMAudioGTTS
from io import BytesIO
from gtts import gTTS

class Client(commands.Bot):

    FFMPEG_PATH = "ffmpeg.exe"
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
        
        sound_fp = BytesIO()
        lang = self.getLanguage(channel.guild.id)
        tts = gTTS(
            text= f'{member.display_name} {self.getConnectedText(lang)}',
            lang= lang,
            tld="us",
            slow=False
        )
        tts.write_to_fp(sound_fp)
        sound_fp.seek(0)
        channel.play(FFmpegPCMAudioGTTS(sound_fp.read(), executable=self.FFMPEG_PATH, pipe=True))

    async def _play_disconnect_sound(self, channel: VoiceClient, member: Member):
        if channel.is_playing():
            channel.stop()
        
        lang = self.getLanguage(channel.guild.id)
        sound_fp = BytesIO()
        tts = gTTS(
            text= f'{member.display_name} {self.getDisonnectedText(lang)}',
            lang= lang,
            tld="us",
            slow=False
        )
        tts.write_to_fp(sound_fp)
        sound_fp.seek(0)
        channel.play(FFmpegPCMAudioGTTS(sound_fp.read(), executable=self.FFMPEG_PATH, pipe=True))
    
    def getLanguage(self, guild_id):
        with open("data.json", "r") as f:
            data = json.load(f)
            lang = None
            try: lang = data[str(guild_id)]["lang"]
            except: pass

            return "hi" if lang is None else lang
        
    def getConnectedText(self, lang: str):
        if lang == "hi":
            return "आ चुके है"
        
        elif lang == "en":
            return "joined"
        
    def getDisonnectedText(self, lang: str):
        if lang == "hi":
            return "जा चुके है"
        
        elif lang == "en":
            return "left"
    
    async def on_guild_join(self, guild: Guild):
        data = {}
        with open("data.json", "r") as f:
            data = json.load(f)

            if str(guild.id) in data.keys():
                data[guild.id]["name"] = guild.name
            else:
                data[guild.id] = {"name": guild.name, "lang":"en"}
        
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)