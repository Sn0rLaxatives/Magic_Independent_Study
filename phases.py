from phase_functions import *
import game_variables


def beginning_phase(player):
    game_variables.number_of_lands_played = 0
    game_variables.castable_types_of_cards = ["Instant"]

    untap_all_cards(player)

    player.draw_card()

def main_phase(player):
    #castable_types_of_cards = ["Land", "Creature", "Instant", "Sorcery", "Enchantment", "Planeswalker"]
    print("Oh yeah we in the main phase of " + player.name)

def combat_phase(player):
    creatures_attacking = declare_attackers(player)

    creatures_blocking = declare_blockers(determine_defending_player(player))


