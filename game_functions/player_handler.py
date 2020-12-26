class player_handler:

    def __init__(self) -> None:
        self.group_1 = set()
        self.group_2 = set()
        self.group_decider = False


    def handle_client(self,player_socket):
        team_name = (player_socket.recv(1024)).decode()
        if self.group_decider:
            self.group_1.add()
        else:
            self.group_2.add(team_name)
        self.group_decider = not self.group_decider
