import os
import game_variables
from deck import Deck
from card import *


def load_deck_files():
    game_variables.dictionary_of_decks = {}

    directory = os.path.dirname(os.path.abspath(__file__))
    deck_file_directory = os.path.join(directory, "deck_information/deck_lists")

    for deck_file in os.listdir(deck_file_directory):
        if deck_file != '.DS_Store':
            with open(os.path.join(deck_file_directory, deck_file), encoding='utf-8') as opened_deck_file:
                opened_deck_file = opened_deck_file.readlines()
                game_variables.dictionary_of_decks[deck_file.rstrip('.txt')] = load_card_information(opened_deck_file)

    return game_variables.dictionary_of_decks


def load_card_information(opened_deck_file):
    card_objects = []

    for card_sheet in opened_deck_file:
        list_card_attributes = card_sheet.split(", ")
        card_objects.append(make_card_objects(list_card_attributes))

    return Deck(card_objects)


def make_card_objects(list_card_attributes):
    card_object = None
    card_name = list_card_attributes[0]
    card_mana_cost = list_card_attributes[1]
    card_type = list_card_attributes[2]
    #card_effect = list_card_attributes[3]

    if card_type == "Creature":
        attack = list_card_attributes[4]
        defense = list_card_attributes[5]
        can_be_blocked_by = list_card_attributes[6]

        #card_object = Creature(card_name, card_mana_cost, card_type, card_effect, attack, defense, can_be_blocked_by)
        card_object = Creature(card_name, card_mana_cost, card_type, attack, defense, can_be_blocked_by)

    elif card_type == "Planeswalker":
        loyalty_counters = list_card_attributes[4]

        #card_object = Planeswalker(card_name, card_mana_cost, card_type, card_effect, loyalty_counters)
    else:
        #card_object = Card(card_name, card_mana_cost, card_type, card_effect)
        card_object = Card(card_name, card_mana_cost, card_type)

    return card_object
