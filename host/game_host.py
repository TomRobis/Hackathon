import threading
from socket import *

from termcolor import colored

import configuration
from host import player_handler
import time


def setup_game_host():
    serverPort = configuration.tcp_port
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    return serverSocket


def start_game():
    server_socket = setup_game_host()
    # event marks the start of assignment of teams to groups
    event = threading.Event()
    p_handler = player_handler.player_handler()
    future = time.time() + configuration.wait_time
    player_threads = []
    while time.time() < future:  # time out - 10 seconds
        try:
            server_socket.settimeout(future - time.time())
            connectionSocket, addr = server_socket.accept()
            # player handler manages the game for the game host - assigns teams to groups and supervises the game
            t = threading.Thread(target=p_handler.handle_client, args=(connectionSocket, event))
            print(colored('a client has been received! hurray!',"magenta"))
            t.start()
            player_threads.append(t)
        except OSError:
            break
    event.set()  # when timeout is reached, assignment to group has ended - p_handler can start the game
    # game over, cleanup
    event.clear()
    server_socket.close()
    for player_thread in player_threads:
        player_thread.join()
