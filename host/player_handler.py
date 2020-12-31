from threading import Lock
from termcolor import colored
import sys
import time

import configuration


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
        """
        once the client is admitted to the game, the following actions occur:
        1. the player's team is assigned to one of two groups
        2. player waits for a set amount of time, until the host begins the game for all players simultaneously.
        3. the player plays the game. score is kept in the corresponding group.
        4. an end game message is sent to the client to let them know the game has ended
        :param player_socket: socket: a line of communication with the client
        :param event: flag that signifies the start of the game
        """
        team_name = (player_socket.recv(configuration.standard_buffer_size)).decode()
        self.room_assignment(team_name)  # teams are assigned to groups in this phase
        event.wait()  # every player waits for 10 seconds to end to start the game, determined by game_host.
        self.play_game(player_socket, team_name)  # all players start to type in characters for 10 secs.
        # we count the scores and determine the winner and then update the players.
        self.send_msg_to_client(self.game_summarize(), player_socket)
        # cleanup and set another game in motion
        player_socket.close()

    def play_game(self, player_socket, team_name):
        """
        after the player receives a message to signify the start of the game,
        they send characters captured by their keyboard over to the host.
        the messages sent are tallied and eventually, the group who has the most clicks wins.
        :param player_socket: socket: a line of communication with the client. clicks are sent via it
        :param team_name: an identifier to which group the player belongs to.
        """
        self.send_msg_to_client(self.welcome_message(), player_socket)
        print(colored('the client has started the game!', "cyan"))
        future = time.time() + configuration.wait_time
        while time.time() < future:  # period of game
            try:
                player_socket.settimeout(future - time.time())
                key = player_socket.recv(configuration.standard_buffer_size)
                if key != b"":  # end of transmission
                    # the clicks counter is a critical section, therefore protected by mutexes
                    if team_name in self.group_1:
                        self.mutex_group1.acquire()
                        self.char_counter_group1 += 1
                        self.mutex_group1.release()
                    else:
                        self.mutex_group2.acquire()
                        self.char_counter_group2 += 1
                        self.mutex_group2.release()
            except OSError:  # the client has disrupted the connection
                pass

            except AttributeError:  # invalid character has been entered.
                continue

    def room_assignment(self, team_name):
        """
        players are split into one of two teams.
        :param team_name: identifier to which group the player belongs.
        """
        self.mutex_group1.acquire()
        if self.group_decider:
            self.group_1.add(team_name)
        else:
            self.group_2.add(team_name)
        self.mutex_group1.release()
        self.group_decider = not self.group_decider

    def welcome_message(self):
        """
        welcome message is built and sent to the client to let them know the game has begun.
        :return: string: said message
        """
        message = "Welcome to Keyboard Spamming Battle Royale.\n"
        message += "Group 1:\n==\n"
        for g in self.group_1:
            message += g
        message += "Group 2:\n==\n"
        for g in self.group_2:
            message += g
        message += "\nStart pressing keys on your keyboard as fast as you can!!"
        return message

    def game_summarize(self):
        """
        end game message is built and sent to the client to let them know the game has ended.
        :return: string: said message
        """
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
        """
        the host sends a message to the client over the tcp connection established
        if the sending is unsuccessful, the game is over and server opens a new game.
        :param msg: str - the message to send to the client
        :param player_socket: - socket : line of communication between player and game host
        """
        try:
            player_socket.send(msg.encode())
        except ConnectionResetError:
            sys.exit()
