import game_variables


def untap_all_cards(player):
    for type_of_card in player.battlefield:
        for card in player.battlefield[type_of_card]:
            card.untap_card()

