import webbrowser, game_variables, game_functions, os, initializing_functions, phases
from tkinter import *
from player import *
from selection_button import *
from deck_information.deck_presentation import *

class StartScreen:
    def __init__(self, master):
        self.start_screen = Toplevel(master=master)
        self.start_screen.title("Start Screen")
        self.master = master
        self.continue_to_game_button = Button(self.start_screen, text="Continue to Game", command=self.close_start_screen)
        self.continue_to_game_button.grid()
        self.how_to_play_button = Button(self.start_screen, text="How to Play", command=self.show_how_to_play)
        self.how_to_play_button.grid()

    def close_start_screen(self):
        self.start_screen.destroy()
        self.dialog_screen = DialogScreen(self.master)

    def show_how_to_play(self):
        webbrowser.open_new("https://www.youtube.com/watch?v=RZyXU1L3JXk")


class DialogScreen:
    def __init__(self, master):
        self.dialog_screen = Toplevel(master=master)
        self.dialog_screen.title("Input Player Data")
        self.master = master
        self.player1_name = ""
        self.player2_name = ""

        Label(self.dialog_screen, text="What is the name of both players?").pack()

        self.player1_entry_box = Entry(self.dialog_screen)
        self.player1_entry_box.pack()
        self.player1_entry_box.insert(0, "Player 1 Name")

        self.player2_entry_box = Entry(self.dialog_screen)
        self.player2_entry_box.pack()
        self.player2_entry_box.insert(0, "Player 2 Name")

        self.submit_names_button = Button(self.dialog_screen, text="Submit Names", command=self.submit_names)
        self.submit_names_button.pack()

    def submit_names(self):
        self.player1_name = self.player1_entry_box.get()
        self.player2_name = self.player2_entry_box.get()

        game_variables.player1 = Player(self.player1_name)
        game_variables.player2 = Player(self.player2_name)

        self.dialog_screen.destroy()
        self.coin_toss_screen = CoinToss(self.master)


class CoinToss:
    def __init__(self, master):
        self.coin_toss_screen = Toplevel(master=master)
        self.master = master

        self.label_string_with_player_name = game_variables.player1.name + " please choose heads or tails."
        self.instruction_label = Label(self.coin_toss_screen, text=self.label_string_with_player_name)
        self.instruction_label.grid(row=0, columnspan=2)

        self.heads_button = Button(self.coin_toss_screen, text="Heads", command=self.player_has_chosen_heads)
        self.heads_button.grid(row=1, column=0)

        self.tails_button = Button(self.coin_toss_screen, text="Tails", command=self.player_has_chosen_tails)
        self.tails_button.grid(row=1, column=1)

    def player_has_chosen_heads(self):
        game_variables.coin_toss = "Heads"
        self.player_made_a_choice()

    def player_has_chosen_tails(self):
        game_variables.coin_toss = "Tails"
        self.player_made_a_choice()

    def player_made_a_choice(self):
        self.coin_toss_screen.destroy()
        game_functions.determine_turn_order(game_variables.player1, game_variables.player2, game_variables.coin_toss)
        self.deck_selection_menu = DeckSelectionMenu(self.master)


class DeckSelectionMenu:
    def __init__(self, master):
        self.master = master
        self.player_selecting = None

        initializing_functions.initialize_decks()

        deck_selection_menu = Toplevel(master=self.master)
        deck_selection_menu.geometry("%dx%d%+d%+d" % (1000, 600, 100, 100))

        self.first_selection_menu(deck_selection_menu)

    def first_selection_menu(self, deck_selection_menu):
        self.player_selecting = game_variables.priority_player

        self.make_containment_frame(self.master, deck_selection_menu)

    def second_selection_menu(self, master, deck_selection_menu):
        self.player_selecting = game_variables.non_priority_player

        DeckSelectionMenu.make_containment_frame(self, master,  deck_selection_menu)

    def make_containment_frame(self, master, deck_selection_menu):
        containment_frame = Frame(deck_selection_menu)
        containment_frame.grid(row=0, column=0)

        title_text = self.player_selecting.name + ", please choose a deck."

        title_label = Label(containment_frame, text=title_text)
        title_label.pack()

        deck_selection_canvas = Canvas(containment_frame, width=1000, height=500, scrollregion=(0, 0, 1200, 500))
        horizontal_scrollbar = Scrollbar(containment_frame, orient=HORIZONTAL)
        horizontal_scrollbar.pack(side=BOTTOM, fill=X)
        horizontal_scrollbar.config(command=deck_selection_canvas.xview)
        deck_selection_canvas.config(width=1000, height=500)
        deck_selection_canvas.config(xscrollcommand=horizontal_scrollbar.set)
        deck_selection_canvas.pack(side=LEFT, expand=True, fill=BOTH)

        DeckSelectionMenu.automate_canvas_deck_selection(self, master, deck_selection_menu, containment_frame, deck_selection_canvas)

    def automate_canvas_deck_selection(self, master, deck_selection_menu, containment_frame, deck_selection_canvas):
        incrementation_modifier = 0

        for deck_being_presented in testing_deck.decks:
            deck_is_not_selected_yet = deck_being_presented in game_variables.dictionary_of_decks
            if deck_being_presented in game_variables.dictionary_of_decks:
                data_incrementation = incrementation_modifier * 200
                deck_image = testing_deck.decks.get(deck_being_presented)

                deck_selection_canvas.create_image(data_incrementation, 50, image=deck_image, anchor=NW)
                deck_selection_canvas.create_text(data_incrementation + 38, 0, text=deck_being_presented, anchor=NW)

                select_button = SelectionButton(master, deck_selection_menu, containment_frame, deck_being_presented, self.player_selecting)
                select_button.configure(width=10, activebackground="#33B5E5", relief=FLAT)
                button1_window = deck_selection_canvas.create_window(data_incrementation + 25, 350, anchor=NW,
                                                                     window=select_button)

                incrementation_modifier += 1

    def select_deck(self, master, deck_selection_menu, containment_frame, deck_name, player_selecting):
        deck_selected = game_variables.dictionary_of_decks[deck_name]
        initializing_functions.set_players_decks(player_selecting, deck_selected)
        del game_variables.dictionary_of_decks[deck_name]

        containment_frame.destroy()

        if player_selecting == game_variables.priority_player:
            DeckSelectionMenu.second_selection_menu(self, master, deck_selection_menu)
        else:
            deck_selection_menu.destroy()
            master.deiconify()
            game_variables.game.start_game()


class GameBoard:

    def __init__(self):
        self.root = Tk()
        testing_deck.initialize_images()
        self.start_screen = StartScreen(self.root)
        self.root.withdraw()

    def show_start_screen(self):
        self.root.mainloop()

    def set_window_size(self):
        self.root.geometry("1366x700")
        self.root.resizable(0, 0)

    def create_gui_layout(self):
        self.game_data_frame = Frame(self.root, height=700, width=100)
        self.game_data_frame.grid(row=0, column=0)

        self.phase_button_frame = Frame(self.root, height=700, width=66, borderwidth=1, relief="solid")
        self.phase_button_frame.grid(row=0, column=1)

        self.game_board_canvas = Canvas(self.root, height=700, width=1190, background="red")
        self.game_board_canvas.grid(row=0, column=2)

        self.add_widgets_to_game_data_frame()
        self.add_widgets_to_phase_button_frame()

    def add_widgets_to_game_data_frame(self):
        self.priority_player_name_label = Label(self.game_data_frame,
                                                text="" + game_variables.priority_player.name)
        self.priority_player_name_label.grid(row=0, column=0)

        self.priority_health = StringVar()
        self.priority_player_health_label = Label(self.game_data_frame, textvariable=self.priority_health)
        self.priority_player_health_label.grid(row=1, column=0)
        self.priority_health.set(game_variables.priority_player.life_total)

        self.nonpriority_player_name_label = Label(self.game_data_frame,
                                                   text="" + game_variables.non_priority_player.name)
        self.nonpriority_player_name_label.grid(row=2, column=0)

        self.non_priority_health = StringVar()
        self.nonpriority_player_health_label = Label(self.game_data_frame, textvariable=self.non_priority_health)
        self.nonpriority_player_health_label.grid(row=3, column=0)
        self.non_priority_health.set(game_variables.non_priority_player.life_total)

        game_variables.player_taking_turn.draw_card()

        self.hand_is_not_showing = True
        self.card_images_from_hand_being_viewed = []
        self.view_hand_button = Button(self.game_data_frame, text="View Hand", command=self.view_hand)
        self.view_hand_button.grid(row=4, column=0)

        self.next_phase_button = Button(self.game_data_frame, text="Next Phase", command=self.next_phase)
        self.next_phase_button.grid(row=5, column=0)
        self.phase_incrementor = 0

    def view_hand(self):
        if self.hand_is_not_showing:
            image_incrementation = 0
            for card in game_variables.player_taking_turn.hand:
                card_on_canvas = self.game_board_canvas.create_image(100 + image_incrementation, 100,
                                                                     image=card.small_image,
                                                                     activeimage=card.regular_image)
                self.card_images_from_hand_being_viewed.append(card_on_canvas)
                image_incrementation += 60
            self.hand_is_not_showing = False
        else:
            for card_from_hand_being_viewed in self.card_images_from_hand_being_viewed:
                self.game_board_canvas.delete(card_from_hand_being_viewed)
            self.hand_is_not_showing = True

    def next_phase(self):
        if self.hand_is_not_showing:
            if self.phase_incrementor == 5:
                self.phase_incrementor = 0
                new_next_player_taking_turn = game_variables.player_taking_turn
                game_variables.player_taking_turn = game_variables.player_not_taking_turn
                game_variables.player_not_taking_turn = new_next_player_taking_turn
                self.current_phase = eval(game_variables.phases_of_turn[self.phase_incrementor])
                self.phase_incrementor +=1
            else:
                self.current_phase = eval(game_variables.phases_of_turn[self.phase_incrementor])
                self.phase_incrementor += 1
        else:
            self.view_hand()
            self.next_phase()

    def add_widgets_to_phase_button_frame(self):
        self.up_arrow_image = PhotoImage(file="utility_images/uparrow.gif")

        self.first_blank_frame = Frame(self.phase_button_frame, height=66, width=66)
        self.first_blank_frame.grid(row=0)

        self.end_phase_button = Button(self.phase_button_frame, text="End Phase")
        self.end_phase_button.grid(row=1)

        self.first_arrow_canvas = Canvas(self.phase_button_frame, height=100, width=66)
        self.first_arrow_canvas.grid(row=2)
        self.first_arrow_canvas.create_image(0, 0, image=self.up_arrow_image, anchor=NW)

        self.second_main_phase_button = Button(self.phase_button_frame, text="2nd Main Phase")
        self.second_main_phase_button.grid(row=3)

        self.second_arrow_canvas = Canvas(self.phase_button_frame, height=100, width=66)
        self.second_arrow_canvas.grid(row=4)
        self.second_arrow_canvas.create_image(0, 0, image=self.up_arrow_image, anchor=NW)

        self.combat_phase_button = Button(self.phase_button_frame, text="Combat Phase")
        self.combat_phase_button.grid(row=5)

        self.third_arrow_canvas = Canvas(self.phase_button_frame, height=100, width=66)
        self.third_arrow_canvas.grid(row=6)
        self.third_arrow_canvas.create_image(0, 0, image=self.up_arrow_image, anchor=NW)

        self.main_phase_button = Button(self.phase_button_frame, text="Main Phase")
        self.main_phase_button.grid(row=7)

        self.fourth_arrow_canvas = Canvas(self.phase_button_frame, height=100, width=66)
        self.fourth_arrow_canvas.grid(row=8)
        self.fourth_arrow_canvas.create_image(0, 0, image=self.up_arrow_image, anchor=NW)

        self.beginning_phase_button = Button(self.phase_button_frame, text="Beginning phase")
        self.beginning_phase_button.grid(row=9)

        self.last_blank_frame = Frame(self.phase_button_frame, height=50, width=66)
        self.last_blank_frame.grid(row=10)

    def update_health_labels(self):
        self.priority_health.set(game_variables.priority_player.life_total)

        self.non_priority_health.set(game_variables.non_priority_player.life_total)

    def start_game(self):
        self.set_window_size()

        self.create_gui_layout()
