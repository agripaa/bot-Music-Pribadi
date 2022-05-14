import discord
from discord.ext.commands import bot
from discord.ext import commands

prefix = "!"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Istri Anijme Sah agripa 😅"))
    print("We have logged in as {0.user}\nHappy dugem. [HALAL!]".format(bot))
#     bot.load_extension('Generalcommand')
    bot.load_extension('Musiccommand')


@bot.event
async def on_message(message):
    client = discord.Client()
    if message.author == client.user:
        return

    if message.content.startswith(prefix+'automatic_play'):
        return
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    await member.send(f'Hi! {member} if u want to hear music with this bot please type **{prefix}play [music]**')


@bot.event
async def on_member_remove(member):
    await member.send(f'Goodbye {member}!')


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
    embed = discord.Embed(title="***Help***", color=0xa09c9c)
#     embed.add_field(name = "General", value = "ping | purge", inline=False)
    embed.add_field(
        name="Music", value="lyric | play | queue | pause | resume", inline=False)
    embed.set_footer(text="Help Menu")
    await ctx.send(embed=embed)

bot.run("TOKEN")
