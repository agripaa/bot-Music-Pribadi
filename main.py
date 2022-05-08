import discord
from discord.ext import commands
from music import Player

itents = discord.Intents.default()
itents.members = True

bot = commands.Bot(command_prefix="!", itents=itents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} siap beraksi")


async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))

bot.loop.create_task(setup())
bot.run('OTcyMTMzNTgyMTA3NzA5NDYw.GB68L5.3AZ1z9DNltREeVtVwlX1tFP4vtwD4dixYlxEJw')
