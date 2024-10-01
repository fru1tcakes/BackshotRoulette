import pyxel




class Toolbar:
    def __init__(self, app, rounds, power_ups=0):
        self.app = app
        self.rounds = rounds
        self.power_ups = power_ups

    def draw_toolbar(self):
        pyxel.rectb(10, 10, 280, 60, 7)
        pyxel.rectb(5, 220, 290, 75, 3)
        self.draw_lives()
        self.draw_shells()
        self.draw_power_ups()
        self.draw_buttons()

    def draw_shells(self):
        live_shell_count = 0
        pyxel.text(130, 25, "LIVE", 6)
        pyxel.text(130, 55, "BLANK", 4)
        blank_shell_count = 0
        for i, shell in enumerate(self.rounds.shells):
            if shell == 1:  # If the shell is live
                # Draw a live shell sprite
                pyxel.blt(150 + live_shell_count * 18, 15, 0, 32, 0, 24, 24)
                live_shell_count += 1
            else:  # If the shell is blank
                # Draw a blank shell sprite
                pyxel.blt(150 + blank_shell_count * 18, 45, 0, 72, 0, 24, 24)
                blank_shell_count += 1

    def draw_lives(self):
        pyxel.text(15, 25, "HEALTH", 7)
        pyxel.text(15, 50, "DEALER", 7)
        for i in range(self.app.player_lives):
            # Draw an image sprite for each life the player has
            # Replace the parameters of pyxel.blt with the correct ones for your image sprite
            # The position of each image is offset by i * 16 to avoid overlap
            pyxel.blt(40 + i * 28, 15, 0, 0, 0, 28, 28)
        for i in range(self.app.dealer.dealer_lives):  # Add this loop to draw the dealer lives
            # Draw an image sprite for each life the dealer has
            pyxel.blt(40 + i * 28, 43, 0, 136, 0, 23, 20)

    def draw_power_ups(self):
        return
        # Code to draw power-ups on the toolbar

    def draw_buttons(self):
        return
        # Code to draw buttons on the toolbar