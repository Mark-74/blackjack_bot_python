import discord, os, random

class gameInstance:
    maxPlayers = 4

    def __init__(self, number_of_players: int) -> None:
        self.number_of_players = number_of_players
        self.players_id = []
        self.player_decks = dict()
        self.dealer_deck = []
        self.current_player = -1
        self.deck = [ 'DA', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DK', 'DQ', #Diamonds
                      'HA', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HK', 'HQ', #Hearts
                      'SA', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SK', 'SQ', #Spades
                      'CA', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CK', 'CQ', #Clubs
                      'DA', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DK', 'DQ', #Diamonds
                      'HA', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HK', 'HQ', #Hearts
                      'SA', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SK', 'SQ', #Spades
                      'CA', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CK', 'CQ', #Clubs
                    ]
        
    def shuffle(self):
        for i in range(len(self.deck)):
            random_pos1, random_pos2 = random.randint(0, len(self.deck)-1), random.randint(0, len(self.deck)-1)
            temp = self.deck[random_pos1]
            self.deck[random_pos1] = self.deck[random_pos2]
            self.deck[random_pos2] = temp
    
    def add(self, player_id: discord.user.User.id) -> bool:
        if not player_id in self.players_id and len(self.players_id) < self.maxPlayers:
            self.players_id.append(player_id)
            return True
        else: return False
    
    def start(self) -> bool:
        if len(self.players_id) != self.number_of_players: return False #cannot start
        self.shuffle()

        for i in range(self.number_of_players):
            self.player_decks[self.players_id[i]] = []
        
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

        for player in self.players_id:
            result += f"{player}, your cards are {self.player_decks[player]}\n"
        return result