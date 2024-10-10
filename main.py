'''
    ____     _       __                        __
   / __/____(_)_  __/ /__________  ____ ______/ /_______
  / /_/ ___/ / / / / __/ ___/ __ \/ __ `/ ___/ //_/ ___/
 / __/ /  / / /_/ / /_(__  ) / / / /_/ / /__/ ,< (__  )
/_/ /_/  /_/\__,_/\__/____/_/ /_/\__,_/\___/_/|_/____/

'''


#######################################  IMPORTS   ##############################################################
import pyxel
import time
from tkinter import *
import dealer
import toolbar
import sys
import round
from achievements import AchievementSystem
from round import Round
from dealer import Dealer
import random
from playsound import playsound
import threading
import atexit
import logging
print(sys.path)
from powerups import PowerUp, Medkit, MagnifyingGlass, Handcuffs
#######################################  LOGGING   ##############################################################

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


#######################################  SOUNDTRACK   ##############################################################
def play_sound():
    # List of songs
    songs = ['osama.mp3', 'wenotlikeyou.mp3', 'withdrawals.mp3']
    random.shuffle(songs)

    for song in songs:
        playsound(song)
        time.sleep(180)

sound_thread = threading.Thread(target=play_sound)
sound_thread.start()
'''
#######################################  SPLASH SCREENS   ##############################################################
splash = Tk()
splash.overrideredirect(True)
splash.title("Welcome")
splash.geometry("1920x1440")
splash.after(4000, splash.destroy)
bg = PhotoImage(file="freaky.png")
lab = Label(splash, image=bg)
lab.pack()

splash.mainloop()

splash2 = Tk()
splash2.overrideredirect(True)
splash2.title("Welcome")
splash2.geometry("300x168+800+500")
splash2.after(4000, splash2.destroy)
bg2 = PhotoImage(file="ya.png")
lab2 = Label(splash2, image=bg2)
lab2.pack()

splash2.mainloop()

dealer_state = 'holdinggun'
'''

#######################################  MAIN GAME   ##############################################################
class App:
    def __init__(self):
        pyxel.init(300, 300, title="Buckshot Roulette")
        pyxel.load("test.pyxres")
        self.rounds = Round()
        self.toolbar = toolbar.Toolbar(self, self.rounds)
        self.rounds.load_shells()
        self.round_number = 1
        self.player_lives = self.round_number * 2
        self.dealer = Dealer(self.player_lives, dealer_state='holdinggun')
        self.bang_time = 0
        self.skip_next_turn = False
        self.click_time = 0
        self.console_messages = []
        self.player_turn = True
        self.dealer_turn_start_time = None
        self.power_ups = []
        self.give_power_ups()
        self.power_up_used_this_turn = False
        self.achievement_system = AchievementSystem()
        self.achievement_system.add_achievement('Beat the Dealer')
        self.achievement_system.add_achievement('Played the game')
        self.achievement_system.save_achievements()
        # Load achievements from file
        self.achievement_system.load_achievements()
        self.achievement_system.earn_achievement('Played the game')
        atexit.register(self.save_and_exit)


        pyxel.run(self.update, self.draw)

    def give_power_ups(self):
        num_power_ups = random.randint(1, 3)
        for _ in range(num_power_ups):
            power_up_type = random.choice([Medkit, MagnifyingGlass, Handcuffs])
            self.power_ups.append(power_up_type())

    def use_power_up(self, power_up_index):
        power_up = self.power_ups[power_up_index]
        if power_up.use(self):
            del self.power_ups[power_up_index]

    def check_button_press(self):
        print (self.power_up_used_this_turn)
        if not self.power_up_used_this_turn:
            if pyxel.btnp(pyxel.KEY_1) and any(isinstance(x, Medkit) for x in self.power_ups):
                self.use_power_up(next(i for i, x in enumerate(self.power_ups) if isinstance(x, Medkit)))
                self.power_up_used_this_turn = True
            elif pyxel.btnp(pyxel.KEY_2) and any(isinstance(x, MagnifyingGlass) for x in self.power_ups):
                self.use_power_up(next(i for i, x in enumerate(self.power_ups) if isinstance(x, MagnifyingGlass)))
                self.power_up_used_this_turn = True
            elif pyxel.btnp(pyxel.KEY_3) and any(isinstance(x, Handcuffs) for x in self.power_ups):
                if self.dealer_turn_start_time is not None:
                    self.use_power_up(next(i for i, x in enumerate(self.power_ups) if isinstance(x, Handcuffs)))
                    self.power_up_used_this_turn = True

    def save_and_exit(self):
        # Save achievements to file
        self.achievement_system.save_achievements()
        logging.info('Achievements saved to file. (Save and Exit)')
        # Exit the Python interpreter
        pyxel.quit()
        sys.exit()

    def add_to_console(self, message):
        # Add a new message to the console
        self.console_messages.append(message)
        self.console_messages = self.console_messages[-7:]
        print(self.console_messages)

    def lose_player_life(self):
        self.player_lives -= 1
        message = f"Player was shot! Remaining lives: {self.player_lives}"
        print(message)
        self.add_to_console(message)

    def update(self):
        if time.time() < self.bang_time + 2 or time.time() < self.click_time + 2:
            return
        if pyxel.btnp(pyxel.KEY_P):
            logging.info('Save and exit trigerred.')
            self.save_and_exit()
        if pyxel.btnp(pyxel.KEY_S):
            logging.info('Manual Save trigerred.')
            self.achievement_system.save_achievements()

        if self.player_lives <= 0 or self.dealer.dealer_lives <= 0:
            self.round_number += 1
            if self.round_number > 3:
                print("Game Over")
                self.achievement_system.earn_achievement('Beat the Dealer')
                pyxel.quit()
            else:
                self.player_lives = self.round_number + 2
                self.dealer.dealer_lives = self.round_number + 2
                self.rounds.reset_shells()  # Reset the shells for the new round
                self.player_turn = True
                self.dealer_turn_start_time = None
                print(f"Round {self.round_number} starts")

        if self.player_turn:
            self.check_button_press()
            self.change_dealer_state('hit')
            if pyxel.btnp(pyxel.KEY_J):
                print("Player decided to shoot himself.")
                current_shell = self.rounds.next_round()
                if current_shell == 1:  # If the shell is live
                    self.lose_player_life()
                    self.bang_time = time.time()
                    self.player_turn = False
                else:  # If the shell was unloaded
                    self.click_time = time.time()
            if pyxel.btnp(pyxel.KEY_L):
                print("Player decided to shoot the dealer.")
                current_shell = self.rounds.next_round()
                if current_shell == 1:
                    self.dealer.lose_life()
                    self.bang_time = time.time()  #
                    self.player_turn = False
                else:
                    self.click_time = time.time()
                    self.player_turn = False
        else:
            if self.skip_next_turn:
                self.skip_next_turn = False
                self.player_turn = True
                self.power_up_used_this_turn = False
            else:
                if self.dealer_turn_start_time is None:
                    self.dealer_turn_start_time = time.time()
                    self.add_to_console("Dealer's turn.")
                    self.change_dealer_state('holdinggun')

            if self.dealer_turn_start_time is not None and time.time() - self.dealer_turn_start_time >= 3:
                live_shells = self.rounds.shells.count(1)
                total_shells = len(self.rounds.shells)
                if total_shells > 0:
                    live_shell_probability = live_shells / total_shells
                else:
                    live_shell_probability = 0

                decision_value = live_shell_probability
                print("Live shell probability:" + str(live_shell_probability))
                print("decision_value" + str(decision_value))

                if decision_value < 0.5:  # If the confidence value is low
                    print("Dealer decided to shoot himself.")
                    self.change_dealer_state('holdinggun')
                    current_shell = self.rounds.next_round()
                    if current_shell == 1:
                        self.dealer.lose_life()
                        self.bang_time = time.time()
                        self.player_turn = True
                        self.add_to_console('The dealer has shot himself.')
                    else:  # If the shell was unloaded
                        self.click_time = time.time()
                        self.player_turn = False
                        self.add_to_console('The dealer has shot himself. It was a Blank Shell.')
                else:  # If the decision value is high
                    print("Dealer decided to shoot the player.")
                    self.change_dealer_state('holdinggun')
                    current_shell = self.rounds.next_round()
                    if current_shell == 1:  # If the shell is live
                        self.lose_player_life()
                        self.bang_time = time.time()
                        self.player_turn = True
                    else:
                        self.click_time = time.time()
                        self.player_turn = True
                        self.add_to_console("Your turn.")

                self.dealer_turn_start_time = None

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(50, 80, 1, 0, 0, 248, 128)
        pyxel.rectb(50, 80, 197, 128, 7)
        pyxel.rectb(0, 0, 300, 300, 7)
        pyxel.text(110, 3, "BACKSHOT ROULETTE", 14)

        self.dealer.draw_dealer()
        self.toolbar.draw_toolbar()

        if time.time() < self.bang_time + 2:
            pyxel.text(106, 118, "BANG!", pyxel.frame_count % 16)
        if time.time() < self.click_time + 2:
            pyxel.text(106, 118, "Click!", pyxel.frame_count % 16)

        for i, message in enumerate(self.console_messages):
            pyxel.text(8, 225 + i * 10, message, 7)

    def change_dealer_state(self, new_state):
        self.dealer.dealer_state = new_state

#######################################  RUN APP & EXCEPTION HANDLING   ##############################################################

app = App()
try:
    pyxel.run(app.update, app.draw)
except SystemExit:
    app.save_and_exit()
except Exception as e:
    print(f"An error occurred: {e}")

