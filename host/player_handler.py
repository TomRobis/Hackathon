import socket
import sys
import time
from threading import Lock


class player_handler:

    def __init__(self) -> None:
        self.group_1 = set()
        self.group_2 = set()
        self.group_decider = False
        # each counter is protected as a critical section, because it could be accessed by multiple threads.
        self.char_counter_group1 = 0
        self.char_counter_group2 = 0
        self.mutex_group1 = Lock()
        self.mutex_group2 = Lock()

    def handle_client(self, player_socket, event):
        team_name = (player_socket.recv(1024)).decode()
        self.room_assignment(team_name)  # teams are assigned to groups in this phase
        event.wait()  # every player waits for 10 seconds to end to start the game, determined by game_host.
        self.play_game(player_socket, team_name)  # all players start to type in characters for 10 secs.
        # we count the scores and determine the winner and then update the players.
        self.send_msg_to_client(self.game_summrize(), player_socket)
        print(self.game_summrize()) #todo
        # cleanup and set another game in motion
        player_socket.close()

    def play_game(self, player_socket, team_name):
        self.send_msg_to_client(self.welcome_message(),player_socket)
        future = time.time() + 10
        while time.time() < future:  # time out
            try:
                player_socket.settimeout(future - time.time())
                key = player_socket.recv(1024)
                if key != b"":
                    if team_name in self.group_1:
                        self.mutex_group1.acquire()
                        self.char_counter_group1 += 1
                        self.mutex_group1.release()
                    else:
                        self.mutex_group2.acquire()
                        self.char_counter_group2 += 1
                        self.mutex_group2.release()
            except OSError:  # timeout
                pass
                # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                # message = template.format(type(ex).__name__, ex.args)
                # print(message)

            except AttributeError:  # invalid character has been entered.
                # or UnicodeDecodeError:
                continue

    def room_assignment(self, team_name):
        self.mutex_group1.acquire()
        if self.group_decider:
            self.group_1.add(team_name)
        else:
            self.group_2.add(team_name)
        self.mutex_group1.release()
        self.group_decider = not self.group_decider

    def welcome_message(self):
        message = "Welcome to Keyboard Spamming Battle Royale.\n"
        message += "Group 1:\n==\n"
        for g in self.group_1:
            message += g
        message += "Group 2:\n==\n"
        for g in self.group_2:
            message += g
        message += "\nStart pressing keys on your keyboard as fast as you can!!"
        return message

    def game_summrize(self):
        to_send = "Game over!\nGroup 1 typed in " + str(self.char_counter_group1) + " characters. Group 2 typed in " + \
                  str(self.char_counter_group2) + " characters.\n"
        if self.char_counter_group1 > self.char_counter_group2:
            to_send += "Group 1 wins!\n\nCongratulations to the winners:\n==\n"
            for team in self.group_1:
                to_send += team
        else:
            to_send += "Group 2 wins!\n\nCongratulations to the winners:\n==\n"
            for team in self.group_2:
                to_send += team
        return to_send

    def send_msg_to_client(self, msg, player_socket):
        try:
            player_socket.send(msg.encode())
        except ConnectionResetError:
            sys.exit()
