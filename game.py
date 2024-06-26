import discord, os, random, datetime


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
        
    def is_game_finished(self) -> bool:
        return self.current_player < self.number_of_players and self.dealer_must_stand()
    
    def get_sum_of(self, player: discord.user.User) -> int:
        sum = 0

        deck = self.player_decks[player]  
        pivot = 1 if deck[0][1] == 'A' and deck[1][1] == 'A' else 2
 
        for i in range(len(deck)):
            sum += self.Value(deck[i]) if i >= pivot else self.Value(deck[i], ace_to_11=True)
        
        if sum > 21 and (deck[0][1] == 'A' or deck[1][1] == 'A'):
            sum = 0
            for card in deck: sum += self.Value(card)
        
        return sum
    
    def get_dealer_sum(self) -> int:
        sum = 0

        deck = self.dealer_deck 
        pivot = 1 if deck[0][1] == 'A' and deck[1][1] == 'A' else 2
 
        for i in range(len(deck)):
            sum += self.Value(deck[i]) if i >= pivot else self.Value(deck[i], ace_to_11=True)
        
        if sum > 21 and (deck[0][1] == 'A' or deck[1][1] == 'A'):
            sum = 0
            for card in deck: sum += self.Value(card)
        
        return sum
    
    def get_dealer_deck(self):
        return self.dealer_deck
    
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
    
    def get_current_player(self) -> discord.User:
        return self.players_user[self.current_player]
    
    def get_deck_from_player(self, player=discord.User) -> str:
        return self.player_decks[player]
    
    def next_player(self) -> bool:
        #returns true if the game can continue, otherwise no
        self.current_player += 1
        return self.current_player < self.number_of_players

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
    
    def take_card(self) -> None:
        self.player_decks[self.players_user[self.current_player]].append(self.deck.pop(0))
        return
    
    def can_continue(self, player: discord.User) -> bool:
        return self.get_sum_of(player=player) < 21
    
    def has_won(self, player: discord.User) -> bool:
        return self.get_sum_of(player=player) == 21
    
    def dealer_must_stand(self):
        return self.get_dealer_sum() >= 17
    
    def dealer_take_card(self):
        if not self.dealer_must_stand():
            self.dealer_deck.append(self.deck.pop(0))