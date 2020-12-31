

class booli_is_back:
    """
        this class represents a boolean variable.
        it is used specifically as stoppage for the keyboard's listener.
    """
    def __init__(self):

        self.game_status = False

    def is_game_over(self):
        """

        :return:
        """
        return self.game_status

    def end_game(self):
        self.game_status = True
