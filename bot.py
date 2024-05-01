import discord, os
from discord.ext import commands
from discord import app_commands
from typing import Optional

token = open('token.txt', 'r').readline()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)

instances = dict()

servers = dict()

#class lobby button
class LobbyButton(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="Enter the lobby",style=discord.ButtonStyle.blurple)
    async def btnEnterLobby(self,interaction:discord.Interaction, button:discord.ui.Button):  #dio cane         
        
        #se il server non è presente nel dizionario server lo aggiungo
        if interaction.guild.id not in servers:
            servers[interaction.guild.id] = interaction.guild.name
        
        instances[interaction.guild_id] = #classe
         
        #prendo l'id dell'utente che preme il bottone, 
        if not instances[interaction.guild_id].add(interaction.user_id):      #se non è presente e la lobby non è piena lo aggiungo altrimenti 
            await interaction.response.send_message("I'm sorry, lobby is full :0")


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
    await interaction.channel.send(view=LobbyButton()) # Send a message with our View class that contains the button

bot.run(token)
