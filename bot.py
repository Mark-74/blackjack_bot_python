import discord, os, game
from discord.ext import commands
from discord import app_commands
from typing import Optional

token = open('token.txt', 'r').readline()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)

instances = dict()

#class lobby button
class LobbyButton(discord.ui.View):
    def __init__(self, *, timeout=60):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="Enter the lobby",style=discord.ButtonStyle.blurple)
    async def btnEnterLobby(self, interaction:discord.Interaction, button:discord.ui.Button):
        if not instances[interaction.guild_id].is_space_available():
                button.disabled = True
                await interaction.response.edit_message(view=self)
                return
        
        if instances[interaction.guild_id].add(interaction.user):
            await interaction.response.send_message(f"{interaction.user.mention} has joined the lobby.")
        else: await interaction.response.send_message("You have already joined the lobby", ephemeral=True)
        
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
async def createLobby(interaction: discord.Interaction):
    if not instances.get(interaction.guild_id):
        instances[interaction.guild_id] = game.gameInstance()
        await interaction.response.send_message(view=LobbyButton())
    else: await interaction.response.send_message("There is already an existing lobby in this server, use ***/newgame*** to create a new lobby.", ephemeral=True)

@bot.tree.command(name='start', description='starts the game.')
async def start(interaction: discord.Interaction):
    if instances[interaction.guild_id].is_playing() is False:
        instances[interaction.guild_id].start()
        await interaction.response.send_message(f"Game has started\n{instances[interaction.guild_id].briefing()}")
        await instances[interaction.guild_id].round(channel=interaction.channel)
    else:
        await interaction.response.send_message("The game has already started, if you wish to restart it, use ***/newgame***", ephemeral=True)

bot.run(token)
