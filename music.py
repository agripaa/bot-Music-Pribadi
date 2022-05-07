import queue
from tkinter import Entry
from webbrowser import get
import discord
import youtube_dl
import asyncio
import pafy
from discord.ext import commands

class Player(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.song_queue = {}
        self.setup()
        
    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []
    
    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)
    
    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format": "bestaudio", "quiet": True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0 : return None
        return [Entry["webpage_url"] for entry in info["entries"]] if get_url else info
    
    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("Luwh kalau mau gw gabung luwh juga harus gabung juga dong nyet!")
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        await ctx.author.voice.channel.connect()
            
    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()
        await ctx.send("Bye bitch")
        
    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("mau denger musik lagi gak ngaf? buru req ajim")
        if ctx.voice_client is None:
            return await ctx.send("Lu kalau mau req musik minimal tau etika lah anj! masukin gw dlu ke room")
        # handle a song where song in url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("bentar dlu gw cari lagu yang lu maksud")
            result = await self.search_song(1, song, get_url=True)
            if result is None:
                return await ctx.send("duh gw gak nemu lagu yang lu maksud, coba masukin judul sama penyanyinya nyet!")
            song = result[0]
        if ctx.voice_client.source is not None :
            queue_len = len(self.song_queue[ctx.guild.id])
            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"")