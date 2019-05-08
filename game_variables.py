from gui import *

player1 = None
player2 = None

coin_toss = None
priority_player = None
non_priority_player = None

player_taking_turn = None
player_not_taking_turn = None

dictionary_of_decks = None

game_stack = []

phases_of_turn = ['phases.beginning_phase(game_variables.player_taking_turn)',
                  'phases.main_phase(game_variables.player_taking_turn)',
                  'phases.combat_phase(game_variables.player_taking_turn)',
                  'phases.main_phase(game_variables.player_taking_turn)',
                  'phases.end_phase(game_variables.player_taking_turn)']

castable_types_of_cards = []
number_of_lands_played_for_turn = 0


game = GameBoard()