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
        self.attacking_creature_identifier = 0
        self.ids = {}
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

        self.game_board_canvas = Canvas(self.root, height=700, width=1190)
        self.game_board_canvas.grid(row=0, column=2)
        self.game_board_canvas.bind('<Button-1>', self.determine_intention_of_click)

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

        self.hand_is_not_showing = True
        self.card_images_from_hand_being_viewed = []
        self.view_hand_button = Button(self.game_data_frame, text="View Hand", command=self.view_hand)
        self.view_hand_button.grid(row=4, column=0)

        self.next_phase_button = Button(self.game_data_frame, text="Next Phase", command=self.next_phase)
        self.next_phase_button.grid(row=5, column=0)
        self.phase_incrementor = 0

        self.player_taking_turn = StringVar()
        self.tracking_whose_taking_turn_label = Label(self.game_data_frame, textvariable=self.player_taking_turn)
        self.tracking_whose_taking_turn_label.grid(row=6)
        self.update_player_taking_turn_label()

        self.amount_of_mana = StringVar()
        self.label_for_amount_of_mana_player_has = Label(self.game_data_frame, textvariable=self.amount_of_mana)
        self.label_for_amount_of_mana_player_has.grid(row=7)
        self.update_amount_of_mana_label()

    def view_hand(self):
        if self.hand_is_not_showing:
            image_incrementation = 0
            for card in game_variables.player_taking_turn.hand:
                card_on_canvas = self.game_board_canvas.create_image(200 + image_incrementation, 350,
                                                                     image=card.small_image,
                                                                     activeimage=card.regular_image)
                self.ids[card_on_canvas] = card
                self.card_images_from_hand_being_viewed.append(card_on_canvas)
                image_incrementation += 90
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
                self.highlight_current_phase(self.phase_incrementor)
                self.set_previous_phase_button_background(5)
                self.refresh_game_canvas()
                self.update_player_taking_turn_label()
                self.update_amount_of_mana_label()
                self.phase_incrementor +=1
            else:
                self.current_phase = eval(game_variables.phases_of_turn[self.phase_incrementor])
                self.highlight_current_phase(self.phase_incrementor)
                self.phase_incrementor += 1
        else:
            self.view_hand()
            self.next_phase()

    def add_widgets_to_phase_button_frame(self):
        self.list_of_phase_buttons = []
        self.up_arrow_image = PhotoImage(file="utility_images/uparrow.gif")

        self.first_blank_frame = Frame(self.phase_button_frame, height=66, width=66)
        self.first_blank_frame.grid(row=0)

        self.end_phase_button = Button(self.phase_button_frame, text="End Phase", command=self.explain_end_phase)
        self.end_phase_button.grid(row=1)

        self.first_arrow_canvas = Canvas(self.phase_button_frame, height=100, width=66)
        self.first_arrow_canvas.grid(row=2)
        self.first_arrow_canvas.create_image(0, 0, image=self.up_arrow_image, anchor=NW)

        self.second_main_phase_button = Button(self.phase_button_frame, text="2nd Main Phase", command=self.explain_main_phase)
        self.second_main_phase_button.grid(row=3)

        self.second_arrow_canvas = Canvas(self.phase_button_frame, height=100, width=66)
        self.second_arrow_canvas.grid(row=4)
        self.second_arrow_canvas.create_image(0, 0, image=self.up_arrow_image, anchor=NW)

        self.combat_phase_button = Button(self.phase_button_frame, text="Combat Phase", command=self.explain_combat_phase)
        self.combat_phase_button.grid(row=5)

        self.third_arrow_canvas = Canvas(self.phase_button_frame, height=100, width=66)
        self.third_arrow_canvas.grid(row=6)
        self.third_arrow_canvas.create_image(0, 0, image=self.up_arrow_image, anchor=NW)

        self.main_phase_button = Button(self.phase_button_frame, text="Main Phase", command=self.explain_main_phase)
        self.main_phase_button.grid(row=7)

        self.fourth_arrow_canvas = Canvas(self.phase_button_frame, height=100, width=66)
        self.fourth_arrow_canvas.grid(row=8)
        self.fourth_arrow_canvas.create_image(0, 0, image=self.up_arrow_image, anchor=NW)

        self.beginning_phase_button = Button(self.phase_button_frame, text="Beginning phase", command=self.explain_beginning_phase)
        self.beginning_phase_button.grid(row=9)

        self.last_blank_frame = Frame(self.phase_button_frame, height=50, width=66)
        self.last_blank_frame.grid(row=10)

        self.list_of_phase_buttons.append(self.beginning_phase_button)
        self.list_of_phase_buttons.append(self.main_phase_button)
        self.list_of_phase_buttons.append(self.combat_phase_button)
        self.list_of_phase_buttons.append(self.second_main_phase_button)
        self.list_of_phase_buttons.append(self.end_phase_button)

    def explain_end_phase(self):
        end_phase_screen = Toplevel(master=self.root)

        explanation_label = Label(end_phase_screen, text="The ending phase is the fifth and final phase of a turn. This is last opportunity for the active player to do anything before passing the turn.")
        explanation_label.grid(row=0)

        close_window_button = Button(end_phase_screen, text="Ok", command=end_phase_screen.destroy)
        close_window_button.grid(row=1)

    def explain_main_phase(self):
        main_phase_screen = Toplevel(master=self.root)

        explanation_label = Label(main_phase_screen,
                                  text="The main phase is both the second and fourth phases of a turn. Non-instants can usually only be played during this phase, only by the active player, and only when the stack is empty. \n The following events occur during the main phase: \n Abilities that trigger at the beginning of the main phase go onto the stack. \n The active player gains priority. \n Once per turn, the active player may play a land from his or her hand during this phase while the stack is empty. \n This is considered a Special Action which does not use the stack. \n Then when both players yield priority in succession while the stack is empty during the pre-combat main phase, the game proceeds to the combat phase. After the combat phase is complete, the game proceeds to the post-combat main phase. \n When both players yield priority in succession while the stack is empty during the post-combat main phase, the game proceeds to the end phase.")
        explanation_label.grid(row=0)

        close_window_button = Button(main_phase_screen, text="Ok", command=main_phase_screen.destroy)
        close_window_button.grid(row=1)

    def explain_combat_phase(self):
        combat_phase_screen = Toplevel(master=self.root)

        explanation_label = Label(combat_phase_screen,
                                  text="The combat phase is the third phase of a turn. In this phase the player may choose to select any non tapped creatures and attack the other player. \n In response the other player may select blockers and determing whom those blockers will block.")
        explanation_label.grid(row=0)

        close_window_button = Button(combat_phase_screen, text="Ok", command=combat_phase_screen.destroy)
        close_window_button.grid(row=1)

    def explain_beginning_phase(self):
        beginning_phase_screen = Toplevel(master=self.root)

        explaining_label = Label(beginning_phase_screen,
                                  text="The beginning phase is the first phase of a turn. In this phase all permanents for the player taking the turn are untapped and that player will draw one card from their deck.")
        explaining_label.grid(row=0)

        close_window_button = Button(beginning_phase_screen, text="Ok", command=beginning_phase_screen.destroy)
        close_window_button.grid(row=1)

    def highlight_current_phase(self, phase_incrementor):
        if phase_incrementor > 0:
            self.set_current_phase_button_background(phase_incrementor)
            self.set_previous_phase_button_background(phase_incrementor)
        else:
            self.set_current_phase_button_background(phase_incrementor)

    def set_current_phase_button_background(self, phase_incrementor):
        current_phase_button = self.list_of_phase_buttons[phase_incrementor]
        current_phase_button.config(highlightbackground="yellow")

    def set_previous_phase_button_background(self, phase_incrementor):
        previous_phase_button = self.list_of_phase_buttons[phase_incrementor - 1]
        previous_phase_button.config(highlightbackground="grey")

    def determine_intention_of_click(self, event):
        canvas_click_index = self.game_board_canvas.find_closest(event.x, event.y)[0]
        self.card_clicked_on = self.ids[canvas_click_index]

        in_combat_phase = self.phase_incrementor == 3
        card_on_players_battlefield = self.card_clicked_on in game_variables.player_taking_turn.battlefield.get("Creature")

        if self.card_clicked_on in game_variables.player_taking_turn.hand:
            self.ask_if_wanting_to_cast(self.card_clicked_on)
        elif in_combat_phase and card_on_players_battlefield:
            self.ask_if_player_wants_this_creature_to_attack(self.card_clicked_on)

    def ask_if_wanting_to_cast(self, card_clicked_on):
        self.ask_if_casting_screen = Toplevel(master=self.root)

        self.label_asking_if_casting = "Are you wanting to cast {}?".format(card_clicked_on)
        self.instruction_label = Label(self.ask_if_casting_screen, text=self.label_asking_if_casting)
        self.instruction_label.grid(row=0, columnspan=2)

        self.yes_button = Button(self.ask_if_casting_screen, text="Yes", command= lambda : game_variables.game.wants_to_cast(card_clicked_on))
        self.yes_button.grid(row=1, column=0)

        self.no_button = Button(self.ask_if_casting_screen, text="No", command=self.ask_if_casting_screen.destroy)
        self.no_button.grid(row=1, column=1)

    def wants_to_cast(self, card_clicked_on):
        self.ask_if_casting_screen.destroy()

        if game_variables.player_taking_turn.mana_in_mana_pool >= card_clicked_on.mana_cost and card_clicked_on.type_of_card in game_variables.castable_types_of_cards:
            if card_clicked_on.type_of_card != "Land":
                game_variables.player_taking_turn.use_mana_from_mana_pool(card_clicked_on.mana_cost)
                game_variables.player_taking_turn.cast_card(card_clicked_on)
            elif game_variables.number_of_lands_played_for_turn == 0:
                game_variables.number_of_lands_played_for_turn += 1
                game_variables.player_taking_turn.cast_card(card_clicked_on)
            else:
                self.warn_card_could_not_be_casted()
        else:
            self.warn_card_could_not_be_casted()

    def warn_card_could_not_be_casted(self):
        cannot_cast_card_screen = Toplevel(master=self.root)

        cannot_cast_label = Label(cannot_cast_card_screen, text="You cannot cast that card at this time.")
        cannot_cast_label.grid(row=0)

        close_window_button = Button(cannot_cast_card_screen, text="Ok", command=cannot_cast_card_screen.destroy)
        close_window_button.grid(row=1)

    def ask_if_player_wants_this_creature_to_attack(self, card_clicked_on):
        self.ask_if_attacking_screen = Toplevel(master=self.root)

        label_asking_if_attacking = "Are you wanting to attack with {}?".format(card_clicked_on)
        instruction_label = Label(self.ask_if_attacking_screen, text=label_asking_if_attacking)
        instruction_label.grid(row=0, columnspan=2)

        yes_button = Button(self.ask_if_attacking_screen, text="Yes",
                                 command= self.set_intention_to_attack_to_true)
        yes_button.grid(row=1, column=0)

        no_button = Button(self.ask_if_attacking_screen, text="No", command=self.set_intention_to_attack_to_false)
        no_button.grid(row=1, column=1)

    def set_intention_to_attack_to_true(self):
        self.process_selected_creature_to_attack(self.card_clicked_on)
        self.ask_if_attacking_screen.destroy()

    def set_intention_to_attack_to_false(self):
        self.ask_if_attacking_screen.destroy()

    def process_selected_creature_to_attack(self, card_clicked_on):
        if card_clicked_on.is_card_tapped:
            self.warn_creature_cannot_attack()
        else:
            game_variables.list_of_attacking_creatures[self.attacking_creature_identifier] = card_clicked_on
            self.attacking_creature_identifier += 1
            self.ask_player_if_done_selecting_attackers()

    def ask_player_if_done_selecting_attackers(self):
        self.done_selecting_attackers_prompt_screen = Toplevel(master=self.root)

        done_selecting_question_label = Label(self.done_selecting_attackers_prompt_screen, text="Are you done selecting creatures to attack with?")
        done_selecting_question_label.grid(row=0, columnspan=2)

        yes_button = Button(self.done_selecting_attackers_prompt_screen, text="Yes", command=self.determine_prompt_for_defensive_player)
        yes_button.grid(row=1, column=0)

        no_button = Button(self.done_selecting_attackers_prompt_screen, text="No", command=self.done_selecting_attackers_prompt_screen.destroy)
        no_button.grid(row=1, column=1)

    def warn_creature_cannot_attack(self):
        cannot_attack_with_creature_screen = Toplevel(master=self.root)

        cannot_cast_label = Label(cannot_attack_with_creature_screen, text="You cannot attack with this creature.")
        cannot_cast_label.grid(row=0)

        close_window_button = Button(cannot_attack_with_creature_screen, text="Ok", command=cannot_attack_with_creature_screen.destroy)
        close_window_button.grid(row=1)

    def determine_prompt_for_defensive_player(self):
        self.done_selecting_attackers_prompt_screen.destroy()
        defending_player_has_blockers = self.does_defensive_player_have_blockers()
        if defending_player_has_blockers:
            self.ask_defensive_player_if_they_will_block()
        else:
            self.warn_defensive_player_of_damage_taken()

    def does_defensive_player_have_blockers(self):
        for creature_card in game_variables.player_not_taking_turn.battlefield.get("Creature"):
            if not creature_card.is_card_tapped:
                return True
        return False

    def ask_defensive_player_if_they_will_block(self):
        self.ask_if_player_will_block_screen = Toplevel(master=self.root)

        instruction_label = Label(self.ask_if_player_will_block_screen, text="Are you wanting to block some/all of the damage?")
        instruction_label.grid(row=0, columnspan=2)

        yes_button = Button(self.ask_if_player_will_block_screen, text="Yes",
                            command=self.ask_if_player_will_block_screen.destroy)
        yes_button.grid(row=1, column=0)

        no_button = Button(self.ask_if_player_will_block_screen, text="No", command=self.close_window_and_warn_of_damage)
        no_button.grid(row=1, column=1)

    def close_window_and_warn_of_damage(self):
        self.ask_if_player_will_block_screen.destroy()
        self.warn_defensive_player_of_damage_taken()

    def warn_defensive_player_of_damage_taken(self):
        damage_taken_screen = Toplevel(master=self.root)

        damage_taken_string = "{} has taken {} damage.".format(game_variables.player_not_taking_turn.name, self.calculate_final_damage())

        cannot_cast_label = Label(damage_taken_screen, text=damage_taken_string)
        cannot_cast_label.grid(row=0)

        close_window_button = Button(damage_taken_screen, text="Ok",
                                     command=damage_taken_screen.destroy)
        close_window_button.grid(row=1)

    def calculate_final_damage(self):
        damage_taken = 0
        for creature_identifier in game_variables.list_of_attacking_creatures:
            damage_taken += int(game_variables.list_of_attacking_creatures.get(creature_identifier).attack)
        game_variables.player_not_taking_turn.subtract_health(damage_taken)
        self.clear_attacking_creatures_list()
        return damage_taken

    def clear_attacking_creatures_list(self):
        game_variables.list_of_attacking_creatures = {}
        self.attacking_creature_identifier = 0

    def refresh_game_canvas(self):
        if self.hand_is_not_showing:
            self.game_board_canvas.delete("all")
            self.place_opponents_creatures()
            self.place_player_taking_turn_creatures()
            self.place_player_taking_turn_enchantments()
            self.place_player_taking_turn_lands()
        else:
            self.view_hand()
            self.refresh_game_canvas()

    def place_opponents_creatures(self):
        image_incrementation = 0
        for card in game_variables.player_not_taking_turn.battlefield.get("Creature"):
            card_on_canvas = self.game_board_canvas.create_image(45 + image_incrementation, 0,
                                                                 image=card.small_image,
                                                                 activeimage=card.regular_image)
            self.ids[card_on_canvas] = card
            image_incrementation += 45

    def place_player_taking_turn_creatures(self):
        image_incrementation = 0
        for card in game_variables.player_taking_turn.battlefield.get("Creature"):
            card_on_canvas = self.game_board_canvas.create_image(150 + image_incrementation, 175,
                                                                 image=card.small_image,
                                                                 activeimage=card.regular_image)
            self.ids[card_on_canvas] = card
            image_incrementation += 45

    def place_player_taking_turn_enchantments(self):
        image_incrementation = 0
        for card in game_variables.player_taking_turn.battlefield.get("Enchantment"):
            card_on_canvas = self.game_board_canvas.create_image(150 + image_incrementation, 350,
                                                                 image=card.small_image,
                                                                 activeimage=card.regular_image)
            self.ids[card_on_canvas] = card
            image_incrementation += 45

    def place_player_taking_turn_lands(self):
        image_incrementation = 0
        for card in game_variables.player_taking_turn.battlefield.get("Land"):
            card_on_canvas = self.game_board_canvas.create_image(150 + image_incrementation, 525,
                                                                 image=card.small_image,
                                                                 activeimage=card.regular_image)
            self.ids[card_on_canvas] = card
            image_incrementation += 45

    def update_health_labels(self):
        self.priority_health.set(game_variables.priority_player.life_total)

        self.non_priority_health.set(game_variables.non_priority_player.life_total)

    def update_player_taking_turn_label(self):
        self.player_taking_turn.set("It is " + game_variables.player_taking_turn.name + "'s turn.")

    def update_amount_of_mana_label(self):
        self.amount_of_mana.set("You have: " + str(game_variables.player_taking_turn.mana_in_mana_pool) + " mana")

    def game_over(self, player):
        game_over_screen = Toplevel(master=self.root)

        game_over_string = player.name + ", lost the game!"
        game_over_label = Label(game_over_screen, text=game_over_string)
        game_over_label.grid(row=1)

    def start_game(self):
        self.set_window_size()

        self.create_gui_layout()
