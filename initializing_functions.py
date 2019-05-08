import game_variables
from player import Player
from initializing_functions_utilities import *


def set_players_decks(player, deck_selected):
    player.setPlayerDeck(deck_selected)

def initialize_decks():
    game_variables.dictionary_of_decks = load_deck_files()

