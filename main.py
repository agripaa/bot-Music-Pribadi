import discord
from discord.ext import commands
import music

cogs = [music]

client = commands.Bot(command_prefix='!', itents = discord.Itents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)


client.run('OTcyMTMzNTgyMTA3NzA5NDYw.GB68L5.3AZ1z9DNltREeVtVwlX1tFP4vtwD4dixYlxEJw')