import discord
import youtube_dl
import asyncio
from youtube_dl import YoutubeDL
from discord.ext import commands


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.MMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.is_playing = False
        self.is_paused = False
        self.vc = None
        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %
                                        item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format": "bestaudio", "quiet": True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0:
            return None
        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.MMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_song(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Paham sopan santun kek anj, minimal gw masukin ke room dlu sat!")
                    return

            else:
                await self.vc.move_to(self.music_queue[0][1])
                self.music_queue.pop(0)
                self.vc.play(discord.FFmpegPCMAudio(
                    m_url, **self.MMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

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
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("masukkan gweh dlu banh dalam room asu!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Lagu yang luwh maksud gak ada di database, coba pake link youtube atau ketik yang bener jangan nyatir!")
            else:
                await ctx.send("dah nih lagu gw masukin list selamat mendengarkan nyet!")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_song(ctx)

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("masukin lagunya jangan lupa nyet!")
        await ctx.send("bentar gw lagi cari dlu lagunya yang lu maksud")
        info = await self.search_song(10, song)
        embed = discord.Embed(
            title=f"hasil lagu yang lu cari : '{song}':", description="*lu bisa gunain link untuk req kalau misalkan lagu yang lu maksud gak sesuai keinginan lu. *\n", colour=discord.Colour.red())
        amount = 0
        for entry in info["entries"]:
            embed.description += f'{entry["title"]}({entry["webpage_url"]})\n'
            amount += 1
        embed.set_footer(
            text=f"menampilkan lagu yang lu maksud {amount}")
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("Lagu lu udah habis nyet gih req lagi")
        embed = discord.Embed(title="antrian lagu",
                              description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{1}) {url}\n"
            i += 1
        embed.set_footer(
            text="Makasih cuy udah make gw jangan lupa follow ig majikan @real.jounny")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("gw gak muterin musik apa apa, beliau skip apaan?")
        if ctx.author.voice is None:
            return await ctx.send("lu aja gak di channel nyet ngapain dah skip'")
        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("gw sekrang gw gak muterin lagu apapun buat lu!")
        poll = discord.Embed(title=f"Yok vote skipnya yang mulai - {ctx.author.name}#{ctx.author.discriminator}",
                             description="**80% dari voice harus setuju kalau musiknya harus di skip. **\n", colour=discord.Colour.blue())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="footing bakalan berhenti dalam waktu 15 detik")
        poll_msg = await ctx.send(embed=poll)
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705")  # yes
        await poll_msg.add_reaction(u"\U0001F6AB")  # no
        await asyncio.sleep(15)
        poll_msg = await ctx.channel.fetch_massage(poll_id)

        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reaction:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)
        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79:
                skip = True
                embed = discord.Embed(title="sudah ke skip, gas cuy lanjut dugem",
                                      description="***Vottingnya dah selesai dengan cara kekeluargaan***", colour=discord.Colour.dark_red())
        if not skip:
            embed = discord.Embed(
                title="skipnya gagal", description="vottingnya gagal ancrit \n sok dah votting ulang")
        embed.set_footer(text="votting selesai!")
        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()
            await self.check_queue(ctx)
