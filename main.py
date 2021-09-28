import datetime
from typing import Text
import discord
from discord import voice_client
from discord.channel import VoiceChannel
import CifradorLuca
import requests
import time
import youtube_dl
import threading

ydl_opts = {
    'outtmpl': "./Music/music.%(ext)s",
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

class MyClient(discord.Client):
    current_vc : voice_client

    async def on_ready(self):
        print("Bot iniciado como", self.user)

        # Setting `Playing ` status
        await self.change_presence(activity=discord.Game(name="nada"))

    async def on_message(self, message):
        # No se responde a si mismo
        if message.author == self.user:
            return

        if message.content.lower().startswith("nashe pone"):
            Cancion = message.content[11:]

            channel : VoiceChannel
            channel = message.author.voice.channel
            connected = False
            
            for member in channel.members:
                if (member.name == "nashe"):
                    connected = True

            if not connected:
                self.current_vc = await channel.connect()

            if Cancion == "":
                await message.channel.send("No pusiste ninguna cancion tilin")
                return
            
            if self.current_vc.is_playing():
                await message.channel.send("Ya esta pusida otra cancion tilin")
                return

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(Cancion, download=True)
                video_title = info_dict.get('title', None)
                video_duration = info_dict.get('duration', None)

                await message.channel.send("Reproduciendo (" + video_title + ", Duracion: " + str(datetime.timedelta(seconds=video_duration)) + ")")
                await self.change_presence(activity=discord.Game(name="escuchando " + video_title))

            self.current_vc.play(discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe", source="./Music/music.mp3"))

        if message.content.lower() == "nashe saca":
            if self.current_vc != None and self.current_vc.is_playing:
                self.current_vc.stop()
                await self.change_presence(activity=discord.Game(name="nada"))
        
        if message.content.lower() == "nashe pausa":
            if self.current_vc != None and self.current_vc.is_playing:
                self.current_vc.pause()
        
        if message.content.lower() == "nashe despausa":
            if self.current_vc != None and self.current_vc.is_playing:
                self.current_vc.resume()

        if message.content == "Nashe Help":
            await message.channel.send("CifradorLuca [Cifrar, Descifrar] [Mensaje], Cifra o Descifra 'mensajes cifrados en Luca'.")
            
        # CifradorLuca
        if "CifradorLuca Cifrar" in message.content:
            Texto = message.content[20:]
            await message.reply("Mensaje Cifrado: " + CifradorLuca.EncryptText(Texto))

        if "CifradorLuca Descifrar" in message.content:
            Texto = message.content[23:]
            await message.reply("Mensaje Descifrado: " + CifradorLuca.DecryptText(Texto))
        # CifradorLuca

client = MyClient()
client.run("ODQwNzM4OTg3MjA3NTU3MTcw.YJclMg.oelafeoLBD9rJ-23xzK45gt2oR0")
