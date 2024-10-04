from tkinter import *
import pickle
import logging
from plyer import notification

class Achievement:
    def __init__(self, name):
        self.name = name
        self.earned = False


class AchievementSystem:
    def __init__(self):
        self.achievements = []

    def add_achievement(self, name):
        self.achievements.append(Achievement(name))

    def earn_achievement(self, name):
        for achievement in self.achievements:
            if achievement.name == name:
                print(f"Earned achievement: {name}")
                if not achievement.earned:
                    achievement.earned = True
                    # Display a notification
                    notification.notify(
                        title="Achievement Earned!",
                        message=f"You have earned the {name} achievement.",
                        app_name="Backshot Roulette",
                        timeout=10
                    )
                break

    def save_achievements(self):
        with open('achievements.pkl', 'wb') as f:
            pickle.dump(self.achievements, f)
            logging.info('Achievements saved to file. (achievements.py)')
            print("Achievements saved to file.")
            notification.notify(
                title="Game saved",
                message=f"Your achievements have been saved.",
                app_name="Backshot Roulette",
                timeout=10
            )


    def load_achievements(self):
        try:
            with open('achievements.pkl', 'rb') as f:
                self.achievements = pickle.load(f)
        except FileNotFoundError:
            print("No achievements file found.")
            pass
