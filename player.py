import game_functions, game_variables
from card_in_transit import *


class Player(object):

    def __init__(self, name_of_player):
        self.name = name_of_player
        self.life_total = 20
        self.mana_in_mana_pool = 100

        self.hand = []
        self.graveyard = []
        self.battlefield = {"Creature": [], "Land": [], "Enchantment": [], "Planeswalker": []}

        self.this_is_first_turn = True

    def setPlayerDeck(self, deck):
        self.deck = deck

    def draw_card(self):
        self.hand.append(self.deck.list_of_cards.pop())

    def cast_card(self, card):
        self.hand.remove(card)
        game_functions.add_to_stack(CardInTransit(game_functions.determine_destination(card), card, self))

