import random

class Round:
    def __init__(self):
        self.current_round = 0
        self.shells = []

    def load_shells(self):
        # Load the shotgun with 5 shells, which are randomly blank (0) or live (1)
        self.shells = [1] + [random.choice([0, 1]) for _ in range(4)]
        random.shuffle(self.shells)  # Shuffle the shells
        # Save the order of the shells
        self.shells_order = self.shells[:]

    def next_round(self):
        # Check if the current shell is live or blank
        if len(self.shells) == 0:
            print("No shells left in the gun. Reloading...")
            self.load_shells()

        # Check if the current shell is live or blank
        current_shell = self.shells[self.current_round]
        if current_shell == 1:
            print("Bang! The shell was live.")
        else:
            print("Click. The shell was blank.")
        # Remove the current shell from the shells list
        self.shells.pop(self.current_round)
        # Return the current shell
        return current_shell

    def peek_next_shell(self):
        # Return the next shell without removing it
        return self.shells[self.current_round]
    def reset_shells(self):
        # Reset the shells
        self.shells = [1] + [random.choice([0, 1]) for _ in range(5)]
        random.shuffle(self.shells)