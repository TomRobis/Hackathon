import threading
import time


class player_handler:

    def __init__(self) -> None:
        self.group_1 = set()
        self.group_2 = set()
        self.group_decider = False
        

    def handle_client(self, player_socket, event):
        team_name = (player_socket.recv(1024)).decode()
        self.room_assignment(team_name)
        event.wait()
        self.play_game(player_socket)
        player_socket.close()

    def play_game(self, player_socket):
        player_socket.send(self.welcome_message().encode())
        future = time.time() + 10
        char_counter = 0
        while time.time() < future:  # time out
            try:
                player_socket.recv(1024)
                char_counter += 1
            except:
                print('some error identification we need to implement later') #todo
        player_socket.send("Game over,sending out offer requests...")




    def room_assignment(self, team_name):
        if self.group_decider:
            self.group_1.add(team_name)
        else:
            self.group_2.add(team_name)
        self.group_decider = not self.group_decider

    def welcome_message(self):
        message = "Welcome to Keyboard Spamming Battle Royale.\n"
        message += "Group 1:\n==\n"
        for g in self.group_1:
            message += g + "\n"
        message += "Group 2:\n==\n"
        for g in self.group_2:
            message += g + "\n"
        message += "Start pressing keys on your keyboard as fast as you can!!"
        return message
