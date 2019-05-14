import game_variables


def untap_all_cards(player):
    for type_of_card in player.battlefield:
        for card in player.battlefield[type_of_card]:
            card.untap_card()

def determine_defending_player(player):
    if player.name == game_variables.player1.name:
        return game_variables.player2
    else:
        return player


def declare_attackers(player):
    selected_creatures = []
    return selected_creatures

def declare_blockers(player):
    selected_creatures = {}
    return selected_creatures