from phase_functions import *
import game_variables


def beginning_phase(player):
    game_variables.number_of_lands_played_for_turn = 0
    game_variables.castable_types_of_cards = ["Instant"]

    untap_all_cards(player)
    if player.this_is_first_turn:
        player.deck.shuffle_deck()
        cards_drawn = 0
        while cards_drawn != 7:
            player.draw_card()
            cards_drawn += 1
        player.this_is_first_turn = False
    else:
        player.draw_card()

def main_phase(player):
    game_variables.castable_types_of_cards = ["Land", "Creature", "Instant", "Sorcery", "Enchantment", "Planeswalker"]
    print("Oh yeah we in the main phase of " + player.name)

def combat_phase(player):
    #creatures_attacking = declare_attackers(player)

    #creatures_blocking = declare_blockers(determine_defending_player(player))
    print("War!")

def end_phase(player):
    print("We are in the endgame now")


