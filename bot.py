import discord, os
from discord.ext import commands
from discord import app_commands
from typing import Optional

token = open('token.txt', 'r').readline()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("BlackJack"))
    synced = await bot.tree.sync()
    print(f"{len(synced)} commands loaded.")
    print(f'We have logged in as {bot.user}')

@bot.tree.command(name='ping', description='replies with pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"pong! requested by {interaction.user.mention}")

@bot.tree.command(name='spooky', description='scares you!')
async def spooky(interaction: discord.Interaction):
    file = discord.File(os.path.join(os.curdir, 'kanye.jpg'), filename="kanye.jpg")
    await interaction.response.send_message(file=file)

@bot.tree.command(name='lobby', description='creates a lobby.')
async def createLobby(interaction: discord.Interaction, number_of_players: int):
    await interaction.response.send_message("under construction")

bot.run(token)
