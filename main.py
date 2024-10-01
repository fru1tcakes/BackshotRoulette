import pyxel
import time
import dealer
import toolbar
import round
from round import Round
from dealer import Dealer
import random

dealer_state = 'holdinggun'


class App:
    def __init__(self):
        pyxel.init(300, 300)
        pyxel.load("test.pyxres")
        self.rounds = Round()
        self.toolbar = toolbar.Toolbar(self, self.rounds)
        self.rounds.load_shells()
        self.player_lives = 3
        self.bang_time = 0  #
        self.dealer = Dealer(self.player_lives, dealer_state='holdinggun')
        self.click_time = 0
        self.console_messages = []
        self.player_turn = True
        self.dealer_turn_start_time = None
        pyxel.run(self.update, self.draw)

    def add_to_console(self, message):
        # Add a new message to the console
        self.console_messages.append(message)
        # Limit the console to the last 10 messages
        self.console_messages = self.console_messages[-7:]
        print(self.console_messages)

    def lose_player_life(self):
        # Decrease the number of lives by one
        self.player_lives -= 1
        message = f"Player was shot! Remaining lives: {self.player_lives}"
        print(message)
        self.add_to_console(message)


    def update(self):
        # If the "BANG!" or "Click!" text is on the screen, return immediately
        if time.time() < self.bang_time + 2 or time.time() < self.click_time + 2:

            return

        if self.player_turn:  # Add this line

            self.change_dealer_state('hit')
            if pyxel.btnp(pyxel.KEY_J):
                print("Player decided to shoot himself.")
                current_shell = self.rounds.next_round()
                if current_shell == 1:  # If the shell is live
                    self.lose_player_life()  # Player loses a life
                    self.bang_time = time.time()  # Set bang_time to the current time
                    self.player_turn = False  # Add this line
                else:  # If the shell was unloaded
                    self.click_time = time.time()  # Set click_time to the current time
            if pyxel.btnp(pyxel.KEY_L):
                print("Player decided to shoot the dealer.")
                current_shell = self.rounds.next_round()
                if current_shell == 1:
                    self.dealer.lose_life()  # Dealer loses a life
                    self.bang_time = time.time()  # Set bang_time to the current time
                else:  # If the shell was unloaded
                    self.click_time = time.time()
                    self.player_turn = False  # Add this line
        else: #  Dealer's turn
            if self.dealer_turn_start_time is None:
                self.dealer_turn_start_time = time.time()
                self.add_to_console("Dealer's turn.")
                self.change_dealer_state('holdinggun')

            if time.time() - self.dealer_turn_start_time >= 3:



                next_shell = self.rounds.peek_next_shell()
                if next_shell == 1:  # If the next shell is live
                    if random.random() < 0.5:  # 50% chance
                        print("Dealer decided to shoot himself.")
                        self.bang_time = time.time()
                        current_shell = self.rounds.next_round()  # This will be a live shell
                        self.dealer.lose_life()  # Dealer loses a life
                        self.bang_time = time.time()  # Set bang_time to the current time
                        self.change_dealer_state('hit')
                        self.player_turn = True
                        self.add_to_console('The dealer has shot himself.')
                        self.add_to_console("Your turn.")
                    else:  # 50% chance
                        print("Dealer decided to shoot the player.")
                        self.bang_time = time.time()
                        current_shell = self.rounds.next_round()  # This will be a live shell
                        self.lose_player_life()  # Player loses a life
                        self.bang_time = time.time()  # Set bang_time to the current time
                else:  # If the next shell is blank
                    if random.random() < 0.7:  # 70% chance
                        print("Dealer decided to shoot himself.")
                        self.change_dealer_state('holdinggun')
                        self.click_time = time.time()
                        self.change_dealer_state('hit')
                        current_shell = self.rounds.next_round()  # This will be a blank shell
                        self.click_time = time.time()  # Set click_time to the current time
                        self.add_to_console('The dealer has shot himself. It was a Blank Shell.')
                    else:  # 30% chance
                        print("Dealer decided to shoot the player.")
                        self.change_dealer_state('holdinggun')
                        self.click_time = time.time()
                        current_shell = self.rounds.next_round()  # This will be a blank shell
                        self.click_time = time.time()  # Set click_time to the current time
                        self.player_turn = True
                        self.add_to_console("Your turn.")

                  # It's now the player's turn
                self.dealer_turn_start_time = None

                pass
    def draw(self):
        pyxel.cls(0)
        pyxel.blt(50, 80, 1, 0, 0, 248, 128)
        pyxel.rectb(50, 80, 197, 128, 7)
        pyxel.rectb(0, 0, 300, 300, 7)
        pyxel.text(110, 3, "BACKSHOT ROULETTE", 14)

        self.dealer.draw_dealer()
        self.toolbar.draw_toolbar()

        # If the current time is less than bang_time plus 2 seconds, display the "BANG!" text
        if time.time() < self.bang_time + 2:
            pyxel.text(106, 118, "BANG!", pyxel.frame_count % 16)
        # If the current time is less than click_time plus 2 seconds, display the "Click!" text
        if time.time() < self.click_time + 2:
            pyxel.text(106, 118, "Click!", pyxel.frame_count % 16)

        for i, message in enumerate(self.console_messages):
            pyxel.text(8, 225 + i * 10, message, 7)

    def change_dealer_state(self, new_state):
        self.dealer.dealer_state = new_state


# Run the app
App()

#pyxel.blt(0, 0, 1, 0, 0, 248, 128)
