import pyxel
import time


class Dealer:
    def __init__(self, dealer_lives=3, dealer_state='normal'):  # Set the default number of dealer lives to 3
        self.dealer_lives = dealer_lives
        self.dealer_state = dealer_state
        self.hit_time = 0

    def lose_life(self):
        self.dealer_lives -= 1
        self.hit_time = time.time()
        print(f"Dealer was shot! Remaining lives: {self.dealer_lives}")
        if self.dealer_lives <= 0:
            self.dealer_state = 'dead'
        else:
            self.dealer_state = 'hit'

    def draw_dealer(self):
        if time.time() < self.hit_time + 2:
            temp_state = 'normal'
        else:
            temp_state = self.dealer_state

        if temp_state == 'normal':
            pyxel.blt(132, 118, 2, 0, 104, 32, 32)
        elif temp_state == 'holdinggun':
            pyxel.blt(132, 113, 2, 0, 0, 40, 40)
        elif temp_state == 'hit':
            pyxel.blt(132, 118, 2, 0, 104, 32, 32)
        elif temp_state == 'dead':
            pyxel.blt(132, 118, 2, 0, 136, 32, 32)