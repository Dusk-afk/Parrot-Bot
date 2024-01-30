from io import BytesIO
from discord import VoiceClient
from gtts import gTTS

from services.db import Db
from services.FFmpegPCMAudioGTTS import FFmpegPCMAudioGTTS

class AudioService:
    FFMPEG_PATH = "ffmpeg"
    
    @staticmethod
    def play_tts(vc: VoiceClient, text: str, lang: str = "en"):
        sound_fp = BytesIO()
        tts = gTTS(
            text= text,
            lang= lang,
            tld="us",
            slow=False
        )
        tts.write_to_fp(sound_fp)
        sound_fp.seek(0)
        vc.play(FFmpegPCMAudioGTTS(sound_fp.read(), executable=AudioService.FFMPEG_PATH, pipe=True))
    
    @staticmethod
    def play_tts_guild(vc: VoiceClient, text: str, guild_id: str):
        lang = Db().of(guild_id).get_language()
        AudioService.play_tts(vc, text, lang)