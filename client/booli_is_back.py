class booli_is_back:
    def __init__(self):
        self.game_status = False

    def is_game_over(self):
        return self.game_status

    def end_game(self):
        self.game_status = True
