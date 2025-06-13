
class GameStats():
    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.reset_stats()
        self.game_active = False
        self.stage = 0


    def reset_stats(self):
        self.stage = 0
