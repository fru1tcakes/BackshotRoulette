
class PowerUp:
    def use(self, app):
        pass

class Medkit(PowerUp):
    def use(self, app):
        if app.player_lives < app.round_number * 2:
            app.player_lives += 1
            return True
        return False

class MagnifyingGlass(PowerUp):
    def use(self, app):
        if app.rounds.shells:
            next_shell = app.rounds.shells[0]
            if next_shell == 1:
                print("The next shell is live.")
                app.add_to_console('The next shell is a Live Shell.')
            else:
                print("The next shell is blank.")
                app.add_to_console('The next shell is a Blank Shell.')
            return True
        return False

class Handcuffs(PowerUp):
    def use(self, app):
        app.skip_next_turn = True
        return True