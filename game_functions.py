import game_variables
from random import *


def determine_turn_order(player1, player2, player1_guess):
    if player1_guess == coin_toss_result():
        game_variables.priority_player = player1
        game_variables.non_priority_player = player2
    else:
        game_variables.priority_player = player2
        game_variables.non_priority_player = player1

    game_variables.player_taking_turn = game_variables.priority_player
    game_variables.player_not_taking_turn = game_variables.non_priority_player


def coin_toss_result():
    toss_value = randint(0, 1)

    if toss_value == 1:
        return "Heads"
    else:
        return "Tails"


def add_to_stack(card_in_transit):
    game_variables.game_stack.append(card_in_transit)
    resolve_stack()


def determine_destination(card):

    if card.type_of_card == "Instant" or card.type_of_card == "Sorcery":
        destination = "graveyard"
    elif card.type_of_card == "Creature":
        destination = "battlefield-Creature"
    elif card.type_of_card == "Land":
        destination = "battlefield-Land"
    elif card.type_of_card == "Enchantment":
        destination = "battlefield-Enchantment"
    else:
        destination = "battlefield-Planeswalker"

    return destination


def resolve_stack():
    while bool(game_variables.game_stack):
        card_being_resolved = game_variables.game_stack.pop()
        # if card_being_resolved.card.card_effect.on_resolve:
        #     card_being_resolved.card.use_ability()
        #     move_card_to_destination(card_being_resolved)
        # else:
        #     move_card_to_destination(card_being_resolved)
        move_card_to_destination(card_being_resolved)

    game_variables.game.refresh_game_canvas()


def move_card_to_destination(card_being_resolved):
    destination = card_being_resolved.destination_of_card
    card = card_being_resolved.card
    owner_of_card = card_being_resolved.owner_of_card

    if destination == "graveyard":
        owner_of_card.graveyard.append(card)
    elif destination == "battlefield-Creature":
        owner_of_card.battlefield.get("Creature").append(card)
    elif destination == "battlefield-Land":
        owner_of_card.battlefield.get("Land").append(card)
    elif destination == "battlefield-Enchantment":
        owner_of_card.battlefield.get("Enchantment").append(card)
    else:
        owner_of_card.battlefield.get("Planeswalker").append(card)
