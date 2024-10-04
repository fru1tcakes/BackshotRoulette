from tkinter import Tk, Label, Button, PhotoImage, Canvas
from achievements import AchievementSystem
import subprocess

class MainMenu:
    def __init__(self, master):
        self.master = master
        master.title("Backshot Roulette")

        self.canvas = Canvas(master, width=800, height=600)
        self.canvas.pack()

        self.bg_image = PhotoImage(file="launcherbg.png")
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image)

        self.start_image = PhotoImage(file="start.png")
        self.start_button = Button(master, image=self.start_image, command=self.start_game, borderwidth=0)
        self.start_button.place(x=80, y=250)

        self.achievements_image = PhotoImage(file="achievements.png")
        self.view_achievements_button = Button(master, image=self.achievements_image, command=self.view_achievements, borderwidth=0)
        self.view_achievements_button.place(x=80, y=300)

        self.exit_image = PhotoImage(file="exit.png")
        self.exit_button = Button(master, image=self.exit_image, command=master.quit, borderwidth=0)
        self.exit_button.place(x=80, y=350)

        self.credits_image = PhotoImage(file="credits.png")
        self.credits_button = Button(master, image=self.credits_image, command=self.view_credits, borderwidth=0)
        self.credits_button.place(x=80, y=400)

    def start_game(self):
        print("Starting game...")
        subprocess.run(["python", "main.py"])

    def view_achievements(self):
        print("Viewing achievements...")
        achievement_system = AchievementSystem()
        achievement_system.load_achievements()
        for achievement in achievement_system.achievements:
            print(f"Achievement: {achievement.name}, Earned: {achievement.earned}")

    def view_credits(self):
        print("Game developed by MDHtrappy")

root = Tk()
main_menu = MainMenu(root)
root.mainloop()