import discord
from discord.ext import commands
from music import Player

itents = discord.Itents.default()
itents.members = True

bot = commands.Bot(command_prefix="!", itents=itents)

@bot.event
async def on_ready():
  print(f"{bot.user.name} siap beraksi")
  
bot.add_cog(Player(bot))
bot.run('OTcyMTMzNTgyMTA3NzA5NDYw.GB68L5.3AZ1z9DNltREeVtVwlX1tFP4vtwD4dixYlxEJw')