import os
import random
import discord
import requests
import json
from replit import db
from discord.ext.commands import bot
from discord.ext import commands

client = discord.Client()
prefix = "!"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help")

sad_words = ["sad", "depresi", "unhappy", "marah",
             "sange", "sirkel", "meninggal", "horny", "loli", "die", "megawati", "bimo pargoy", "segs", "mabar", "pagi", "siang", "malam", "voice", "ingfo ingfo", "banh", "ikut", "genshin"]
starter_encouragements = [
    "Mampus!",
    "Semangat!",
    "You are a great person",
    "Lu tuh gak di ajak",
    "lol",
    "alhamdullilah",
    "astagfirullah",
    "UWOGGGGGGGGGGHHHHHHHHHHH SEGGGGGGGGGGGGGSSSSSSSSSSSSS",
    "WANGGYYYYYYYYYYYYYYYY",
    "CAN I CALL FBI?",
    "BAKSOOO BAKSOOOOO",
    "gas mabar",
    "mending sekarang lu diem",
    "gasss kuyyyyy",
    "maszehhhhh maszehhhhh",
    "luwh psatir bang?",
    "AJIM AJIM AJIM BANGET AJIM BANGET",
    "IKODDDDDDDD",
    "Game 4nooooooo",
    "Luwh anijme bang?",
    "follow instagram @real_jounny"
]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragements(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Maintenance"))
    print("We have logged in as {0.user}\nHappy dugem. [HALAL!]".format(bot))
#     bot.load_extension('Generalcommand')
    bot.load_extension('Musiccommand')


@bot.event
async def on_member_join(member):
    await member.send(f'Hi! {member} if u want to hear music with this bot please type **{prefix}play [music]**')


@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith(prefix+'automatic_play'):
        return
    await bot.process_commands(message)


@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith("!quote"):
        quote = get_quote()
        return await message.channel.send(quote)
    options = starter_encouragements
    if "encouragements" in db.keys():
        options = options + db["encouragements"]
    if any(word in msg for word in sad_words):
        return await message.channel.send(random.choice(options))
    if msg.startswith('!new'):
        encouraging_message = msg.split('!new', 1)[1]
        update_encouragements(encouraging_message)
        return await message.channel.send("Jawaban dari bot sudah ditambahkan!")
    if msg.startswith('!del'):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("!del", 1)[1])
            delete_encouragements(index)
            encouragements = db["encouragements"]
        return await message.channel.send(encouragements)
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.qualified_name == "play":
            await ctx.send(f"{prefix}play [query|link musik]")
        else:
            await ctx.send("Missing required argument!")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command is unreachable")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have enough permission!")


@bot.command(invoke_without_command=True)
async def help(ctx):
    tip = [" - !play (query or link) to play a music", " - DM iFanpS#5409 if u want to contribute", " - Use headphone for better experience"
           " - Don't leave while bot is playing a music, bot will sad ;(", " - Listening music together will be fun 🥳"]
    await ctx.send("Tip"+random.choice(tip)+"\n")
    embed = discord.Embed(title="***Help***", color=0xa09c9c)
    embed.add_field(name="General", value="ping | purge", inline=False)
    embed.add_field(
        name="Music", value="lyric | play | stop | queue | pause | resume", inline=False)
    embed.set_footer(text="Help Menu")
    await ctx.send(embed=embed)

bot.run("OTcyMTMzNTgyMTA3NzA5NDYw.GDDY0V.dWN5c0jDSS2zFdyUis-H051T_T5Agpf6fBjwT4")
