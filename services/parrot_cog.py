import asyncio
import json
import random
from gtts import gTTS
from io import BytesIO
from discord import Interaction, ButtonStyle, VoiceChannel, VoiceState
from discord.ext.commands import Cog, command, Context
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord import Interaction, SelectOption
from discord.commands.context import ApplicationContext
from discord.ui import Button, View, select
from discord.ui.select import Select
from discord.commands import slash_command
from services.FFmpegPCMAudioGTTS import FFmpegPCMAudioGTTS

guild_ids = [597112845221494784, 955048661132406845]

class LanguageSelectMenu(View):
    @select(placeholder="Select the language", options=[
        SelectOption(label="Hindi", emoji="🇮🇳"),
        SelectOption(label="English", emoji="🇺🇸"),
    ])

    async def callback(self, select: Select, interaction: Interaction):
        selected = select.values[0]
        if selected == "Hindi":
            self.changeLanguage("hi", interaction.guild_id)
        elif selected == "English":
            self.changeLanguage("en", interaction.guild_id)

        await interaction.response.edit_message(content= f"Language Changed to {selected} ✅", view=None)
    
    def changeLanguage(self, lang: str, guild_id: int):
        data = {}
        with open("data.json", "r") as f:
            data = json.load(f)
            if str(guild_id) not in data.keys():
                data[str(guild_id)] = {"lang": lang}
            else:
                data[str(guild_id)]["lang"] = lang
        
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

class ParrotCog(Cog):
    FFMPEG_PATH = "ffmpeg.exe"

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="start", description="Connects Parrot to your current voice channel", guild_ids = guild_ids)
    async def start(self, ctx: ApplicationContext):
        voice = ctx.author.voice

        if voice is None:
            await ctx.respond("Looks like you're not in a voice channel")
            return
        
        try:
            vc = await voice.channel.connect()
            await ctx.respond(self.bot.user.name + " is connected to " + voice.channel.name + " 👌")
            await self.doIntro(vc)
        except Exception as e:
            print(e)
            await ctx.respond("Looks like I'm already in a voice channel.\nIf not then try again after a minute.")
    
    @slash_command(name="test", description="For testing purpose", guild_ids = guild_ids)
    async def test(self, ctx: ApplicationContext):
        await ctx.respond("Yes, I'm alive")
    
    @slash_command(name="stop", description="Disconnects Parrot from voice channel", guild_ids = guild_ids)
    async def stop(self, ctx: ApplicationContext):
        try:
            await ctx.voice_client.disconnect()
            await ctx.respond("Bye 👋")
        except Exception as e:
            print(e)

    @slash_command(name="config", description="This command allows you to manage settings for Parrot", guild_ids = guild_ids)
    async def config(self, ctx: ApplicationContext):
        lang_btn = Button(
            label="Language",
            style= ButtonStyle.gray,
            emoji="🌐"
        )
        lang_btn.callback = self.configLangCallback

        view = View()
        view.add_item(lang_btn)
        await ctx.respond("", view=view)

    async def configLangCallback(self, interaction: Interaction):
        await interaction.response.edit_message(content="", view=LanguageSelectMenu())
    
    # @slash_command(name="join", guild_ids = guild_ids)
    # async def join(self, ctx: ApplicationContext):
    #     await ctx.respond("Join!")
    
    @slash_command(name="hello", description="Test if the parrot can speak", guild_ids = guild_ids)
    async def hello(self, ctx: ApplicationContext):
        for vc in self.bot.voice_clients:
            vc: VoiceClient = vc
            if ctx.author.voice != None:
                if vc.channel.id == ctx.author.voice.channel.id:
                    await self.doIntro(vc)
                    await ctx.respond("Greeting you in " + vc.channel.name)
                    return

        await ctx.respond("I am not connected to your voice channel", ephemeral = True)
        
        
    
    async def doIntro(self, vc: VoiceClient):
        lang = self.getLanguage(vc.guild.id)
        script = ""

        if lang == "hi":
            intros_hi = ["अरे ओपी बोलते क्या", "अरे जॉड बोलते क्या", "अरे नहीं होरा क्या", "ahahahahahahahaha", "kehndi hundi see"]
            script = random.choice(intros_hi)
        
        elif lang == "en":
            script = "Hi, I am here at your service"
        
        sound_fp = BytesIO()
        tts = gTTS(
            text= script,
            lang= lang,
            tld="us",
            slow=False
        )
        tts.write_to_fp(sound_fp)
        sound_fp.seek(0)
        vc.play(FFmpegPCMAudioGTTS(sound_fp.read(), executable=self.FFMPEG_PATH, pipe=True))

    @slash_command(name="say", description="Parrot will repeat your message", guild_ids = guild_ids)
    async def say(self, ctx: ApplicationContext, text: str):
        for vc in self.bot.voice_clients:
            vc: VoiceClient = vc
            if ctx.author.voice != None:
                if vc.channel.id == ctx.author.voice.channel.id:
                    try:
                        self.tts(text, vc)
                        await ctx.respond("Repeated your text in " + vc.channel.name + "\n > " + text)
                    except:
                        ctx.respond("Please wait for me to stop", ephemeral = True)
                    finally:
                        return

        await ctx.respond("I am not connected to your voice channel", ephemeral = True)
    
    @slash_command(name="shutup", description="Parrot will shutup", guild_ids = guild_ids)
    async def shutup(self, ctx: ApplicationContext):
        for vc in self.bot.voice_clients:
            vc: VoiceClient = vc
            if ctx.author.voice != None:
                if vc.channel.id == ctx.author.voice.channel.id:
                    vc.stop()
                    await ctx.respond("Stopped speaking in " + vc.channel.name, ephemeral = True)
                    return

        await ctx.respond("I am not connected to your voice channel", ephemeral = True)
    
    def tts(self, text: str, vc: VoiceClient):
        sound_fp = BytesIO()
        tts = gTTS(
            text= text,
            lang= self.getLanguage(vc.guild.id),
            tld="us",
            slow=False
        )
        tts.write_to_fp(sound_fp)
        sound_fp.seek(0)
        vc.play(FFmpegPCMAudioGTTS(sound_fp.read(), executable=self.FFMPEG_PATH, pipe=True))
        
    def getLanguage(self, guild_id):
        with open("data.json", "r") as f:
            data = json.load(f)
            lang = None
            try: lang = data[str(guild_id)]["lang"]
            except: pass

            return "hi" if lang is None else lang