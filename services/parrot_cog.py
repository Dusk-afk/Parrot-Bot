import random
from gtts import gTTS
from io import BytesIO
from discord import Interaction, ButtonStyle, VoiceChannel, VoiceState, Embed, Colour
from discord.ext.commands import Cog, command, Context, has_permissions
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord import Interaction, SelectOption
from discord.commands.context import ApplicationContext
from discord.ui import Button, View, select
from discord.ui.select import Select
from discord.commands import slash_command
from services.FFmpegPCMAudioGTTS import FFmpegPCMAudioGTTS
from services.audio_service import AudioService
from services.db import Db 

guild_ids = None
# guild_ids = [1063893968418504764]

class LanguageSelectMenu(View):
    @select(placeholder=f"Select the language", options=[
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
        Db().of(guild_id).set_language(lang)

class ParrotCog(Cog):
    FFMPEG_PATH = "ffmpeg.exe"

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="start", description="Connects Parrot to your current voice channel", guild_ids=guild_ids)
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
    
    @slash_command(name="test", description="For testing purpose", guild_ids=guild_ids)
    async def test(self, ctx: ApplicationContext):
        await ctx.respond("Yes, I'm alive")
    
    @slash_command(name="stop", description="Disconnects Parrot from voice channel", guild_ids=guild_ids)
    async def stop(self, ctx: ApplicationContext):
        try:
            await ctx.voice_client.disconnect()
            await ctx.respond("Bye 👋")
        except Exception as e:
            print(e)

    @slash_command(name="config", description="This command allows you to manage settings for Parrot", guild_ids=guild_ids)
    async def config(self, ctx: ApplicationContext):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You are not authorized to use this command", ephemeral = True)
            return

        lang_btn = Button(
            label="Language",
            style= ButtonStyle.gray,
            emoji="🌐"
        )
        lang_btn.callback = self.configLangCallback

        say_value = "Disabled" if self.isSayDisabled(ctx.guild_id) else "Enabled"
        say_btn = Button(
            label= f"Toggle Say: {say_value}",
            style= ButtonStyle.gray,
            emoji="🗣"
        )
        say_btn.callback = self.configSayCallback

        view = View()
        view.add_item(lang_btn)
        view.add_item(say_btn)
        await ctx.respond("", view=view, ephemeral = True)

    async def configLangCallback(self, interaction: Interaction):
        if not interaction.permissions.administrator:
            await interaction.response.send_message("You are not authorized to interact", ephemeral = True)
            return
        await interaction.response.edit_message(content="", view=LanguageSelectMenu())
    
    async def configSayCallback(self, interaction: Interaction):
        if not interaction.permissions.administrator:
            await interaction.response.send_message("You are not authorized to interact", ephemeral = True)
            return

        currently_say_disabled = self.isSayDisabled(interaction.guild_id)

        Db().of(interaction.guild_id).set_say_enabled(not currently_say_disabled)

        lang_btn = Button(
            label="Language",
            style= ButtonStyle.gray,
            emoji="🌐"
        )
        lang_btn.callback = self.configLangCallback

        say_value = "Disabled" if not currently_say_disabled else "Enabled"
        say_btn = Button(
            label= f"Toggle Say: {say_value}",
            style= ButtonStyle.gray,
            emoji="🗣"
        )
        say_btn.callback = self.configSayCallback

        view = View()
        view.add_item(lang_btn)
        view.add_item(say_btn)

        final_msg = "Say disabled" if not currently_say_disabled else "Say enabled"
        await interaction.response.edit_message(content= final_msg , view=view)
    
    def isSayDisabled(self, guild_id):
        return not Db().of(guild_id).is_say_enabled()
    
    @slash_command(name="hello", description="Test if the parrot can speak", guild_ids=guild_ids)
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
            intros_en = ["hey, there","i, am just like jarvis. but only if he was from wallmart","dude this server makes me feel alive","do you know? siri and i are both cousins"]
            script = random.choice(intros_en)

        AudioService.play_tts(vc, script, lang)

    @slash_command(name="say", description="Parrot will repeat your message", guild_ids=guild_ids)
    async def say(self, ctx: ApplicationContext, text: str):
        if self.isSayDisabled(ctx.guild_id):
            await ctx.respond("Say is currently disabled. To enable it you can ask the admin.", ephemeral = True)
            return

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
    
    @slash_command(name="shutup", description="Parrot will shutup", guild_ids=guild_ids)
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
        AudioService.play_tts(vc, text, self.getLanguage(vc.guild.id))
        
    def getLanguage(self, guild_id):
        return Db().of(guild_id).get_language()
    
    @slash_command(name="help", description="Shows a list of commands that you can use for Parrot", guild_ids=guild_ids)
    async def help(self, ctx: ApplicationContext):
        script = (
            "/config: This command allows you to manage settings for Parrot\n"
            "/hello: You can check if the Parrot can speak\n"
            "/help: You will see this message\n"
            "/say: Parrot will say what you type\n"
            "/start: Parrot will join your current voice channel\n"
            "/shutup: Parrot will stop talking\n"
            "/stop: Parrot will leave the voice channel\n"
            "/test: For testing purpose"
        )
        embed = Embed(
            title="All the commands",
            description= script,
            color=Colour.from_rgb(25, 34, 65)
        )
        await ctx.respond(embed=embed)