import discord, os, game, time
from discord.ext import commands
from discord import app_commands
from discord.ui import View
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

class Choices(discord.ui.View):
    def __init__(self, *, timeout=None):
            super().__init__(timeout=timeout)
    
    @discord.ui.button(label="Take", emoji='🃏', custom_id='choice-take', style=discord.ButtonStyle.success)
    async def btnTake(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user == instances[interaction.guild_id].get_current_player():
            curr = instances[interaction.guild_id]
            player = curr.get_current_player()

            if curr.has_won(interaction.user):
                print("won")
                await self.btnKeep.callback(interaction=interaction)
                return
            
            curr.take_card()

            if curr.can_continue(player=player):
                embed = interaction.message.embeds.pop(0).remove_field(0).add_field(name="Your cards", value=curr.get_deck_from_player(player=player), inline=False)
                await interaction.response.edit_message(embed=embed)

            else:
                embed = interaction.message.embeds.pop(0).remove_field(0).add_field(name="Your cards", value=curr.get_deck_from_player(player=player), inline=False)
                await interaction.response.edit_message(embed=embed, view=None)
                await self.btnKeep.callback(interaction=interaction)
                
        else:
            await interaction.response.send_message("Wait for your turn!", ephemeral=True)

    
    @discord.ui.button(label="Keep", emoji='🖐', custom_id='choice-keep', style=discord.ButtonStyle.danger)
    async def btnKeep(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user == instances[interaction.guild_id].get_current_player():
            #if interaction.message.components.count(discord.ui.Button) != 0: await interaction.response.edit_message(view=None)
            try:
                await interaction.response.edit_message(view=None)
            except:
                pass
            
            if instances[interaction.guild_id].next_player():
                await round(interaction=interaction)
            else:
                await dealer_round(interaction=interaction) #TODO: send results
        else: 
            await interaction.response.send_message("Wait for your turn!", ephemeral=True)

    @discord.ui.button(label="Double", emoji='💸', custom_id='choice-double', style=discord.ButtonStyle.blurple)
    async def btnDouble(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user == instances[interaction.guild_id].get_current_player():
            curr = instances[interaction.guild_id]
            player = curr.get_current_player()

            if curr.has_won(interaction.user):
                print("won")
                await self.btnKeep.callback(interaction=interaction)
                return
            
            curr.take_card()
            embed = interaction.message.embeds.pop(0).remove_field(0).add_field(name="Your cards", value=curr.get_deck_from_player(player=player), inline=False)
            await interaction.response.edit_message(embed=embed, view=None)
            await self.btnKeep.callback(interaction=interaction)
                
        else:
            await interaction.response.send_message("Wait for your turn!", ephemeral=True)

    async def on_timeout(self) -> None:
        print("timed out")
        
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

async def round(interaction: discord.Interaction) -> bool:
        
    curr = instances[interaction.guild_id]
    player = curr.get_current_player()

    View = Choices()
    embed = discord.Embed(title=f"{player}'s hand", description="Take a close look at your **cards** and decide what to do next!", color=0x5738d2) #TODO: add timestamp
    embed.add_field(name="Your cards", value=curr.get_deck_from_player(player=player), inline=False)
    embed.set_footer(text="---------------------------------------------------------------------------------")
    await interaction.channel.send(content=f"{player.mention} would you like another card?", embed=embed, view=View)

async def dealer_round(interaction: discord.Interaction):
    curr = instances[interaction.guild_id]
    message = await interaction.channel.send("Dealer's turn!")

    while(True):
        embed = embed = discord.Embed(title=f"Dealer's hand", color=0x5738d2)
        embed.add_field(name="Dealer's cards", value=curr.get_dealer_deck(), inline=False)
        embed.set_footer(text="---------------------------------------------------------------------------------")
        message = await message.edit(embed=embed)

        time.sleep(1)
        if curr.dealer_must_stand():
            break #game has ended
        else:
            curr.dealer_take_card()

@bot.tree.command(name='start', description='starts the game.')
async def start(interaction: discord.Interaction):
    if instances.get(interaction.guild_id):
        if instances[interaction.guild_id].is_playing() is False:
            instances[interaction.guild_id].start()
            await interaction.response.send_message(f"Game has started\n{instances[interaction.guild_id].briefing()}")
            await round(interaction=interaction)
        else:
            await interaction.response.send_message("The game has already started, if you wish to restart it, use ***/newgame***", ephemeral=True)
    else:
        await interaction.response.send_message("There isn't a lobby yet, create one with ***/lobby***", ephemeral=True)
bot.run(token)
