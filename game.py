import discord, os, random
from discord.ui import View

class YesButton(discord.ui.View):
        def __init__(self, *, timeout=60):
            super().__init__(timeout=timeout)
        
        @discord.ui.button(label="Pick 🃏", custom_id='yes', style=discord.ButtonStyle.success)
        async def btnYes(self, interaction:discord.Interaction, button:discord.ui.Button):
            pass

class NoButton(discord.ui.View):
    def __init__(self, *, timeout=60):
        super().__init__(timeout=timeout)
        
    @discord.ui.button(label="Pick 🃏", custom_id='no', style=discord.ButtonStyle.danger)
    async def btnNo(self, interaction:discord.Interaction, button:discord.ui.Button):
        pass

    async def on_timeout(self) -> None:
        pass


class gameInstance:
    maxPlayers = 4

    def __init__(self) -> None:
        self.number_of_players = 0
        self.players_user = []
        self.player_decks = dict() #discord.user.User -> list[str]
        self.dealer_deck = []
        self.current_player = 0
        self.status = False #is_playing
        self.deck = [ 'DA', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DK', 'DQ', #Diamonds
                      'HA', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HK', 'HQ', #Hearts
                      'SA', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SK', 'SQ', #Spades
                      'CA', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CK', 'CQ', #Clubs
                      'DA', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DK', 'DQ', #Diamonds
                      'HA', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HK', 'HQ', #Hearts
                      'SA', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SK', 'SQ', #Spades
                      'CA', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CK', 'CQ', #Clubs
                    ]
    
    @staticmethod
    def Value(card: str, ace_to_11 = False) -> int:
        if card[1] == 'A':
            if ace_to_11: return 11
            else: return 1
        elif card[1] == 'J' or card[1] == 'K' or card[1] == 'Q':
            return 10
        else: 
            return int(card[1:])
        
    def get_sum_of(self, player: discord.user.User):
        sum = 0

        deck = self.player_decks[player]  
        pivot = 1 if deck[0][1] == 'A' and deck[1][1] == 'A' else 2
 
        for i in range(len(deck)):
            sum += self.Value(deck[i]) if i >= pivot else self.Value(deck[i], ace_to_11=True)
        
        if sum > 21 and (deck[0][1] == 'A' or deck[1][1] == 'A'):
            sum = 0
            for card in deck: sum += self.Value(card)
        
        return sum
     
    def shuffle(self):
        for i in range(len(self.deck)):
            random_pos1, random_pos2 = random.randint(0, len(self.deck)-1), random.randint(0, len(self.deck)-1)
            temp = self.deck[random_pos1]
            self.deck[random_pos1] = self.deck[random_pos2]
            self.deck[random_pos2] = temp
    
    def add(self, player: discord.user.User) -> bool:
        if not player in self.players_user and len(self.players_user) < self.maxPlayers:
            self.players_user.append(player)
            self.number_of_players += 1
            return True
        else: return False
    
    def is_space_available(self) -> bool:
        #returns true if there's space, else returns false
        return self.maxPlayers != len(self.players_user) and self.is_playing() is False 
    
    def is_playing(self) -> bool:
        return self.status

    def start(self) -> bool:
        self.status = True #update status
        self.shuffle()

        for i in range(self.number_of_players):
            self.player_decks[self.players_user[i]] = []
        
        #give 2 cards to each player
        for deck in self.player_decks.values():
            deck.append(self.deck.pop(0))
            deck.append(self.deck.pop(0))
        
        #dealer included
        self.dealer_deck.append(self.deck.pop(0))
        self.dealer_deck.append(self.deck.pop(0))

        return True

    def briefing(self) -> str:
        result = ""

        for player in self.players_user:
            result += f"{player.mention}, your cards are {self.player_decks[player]}\n"
        return result
    
    async def round(self, interaction: discord.Interaction) -> bool:
        
        #returns true if the game continues, else returns false
        
        view = View()
        view.children.append(YesButton())
        view.children.append(NoButton())

        await interaction.channel.send(content=f"{self.players_user[self.current_player].mention} would you like another card?", view=view)