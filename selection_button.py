import gui
from tkinter import *


class SelectionButton(Button):
    def __init__(self, master, deck_selection_menu, containment_frame, deck_name, player_selecting):
        Button.__init__(self, containment_frame, text="Select",
                        command=lambda: gui.DeckSelectionMenu.select_deck(self, master, deck_selection_menu, containment_frame, deck_name, player_selecting), anchor=W)

