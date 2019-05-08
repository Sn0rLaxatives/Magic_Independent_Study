from random import shuffle
class Deck(object):
    def __init__(self, list_of_cards):
        self.list_of_cards = list_of_cards

    def shuffle_deck(self):
        shuffle(self.list_of_cards)
