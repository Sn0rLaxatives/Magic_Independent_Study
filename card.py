import card_effects, tkinter


class Card(object):

    def __init__(self, name_of_card, mana_cost, type_of_card, card_effect):
        self.name_of_card = name_of_card
        self.mana_cost = mana_cost
        self.type_of_card = type_of_card
        self.is_card_tapped = False
        self.card_effect = getattr(card_effects, card_effect)
        self.small_image = tkinter.PhotoImage(file="small_card_images/" + self.name_of_card + ".gif")
        self.regular_image = tkinter.PhotoImage(file="regular_card_images/" + self.name_of_card + ".gif")

    def tap_card(self):
        self.is_card_tapped = True

    def untap_card(self):
        self.is_card_tapped = False

    def use_ability(self):
        self.card_effect()


class Creature(Card):
    def __init__(self, name_of_card, mana_cost, type_of_card, card_effect, attack, defense, can_be_blocked_by):
        super().__init__(name_of_card, mana_cost, type_of_card, card_effect)
        self.attack = attack
        self.defense = defense
        self.can_be_blocked_by = can_be_blocked_by


class Planeswalker(Card):
    def __init__(self, name_of_card, mana_cost, type_of_card, card_effect, loyalty_counters):
        super().__init__(name_of_card, mana_cost, type_of_card, card_effect)
        self.loyalty_counters = loyalty_counters
