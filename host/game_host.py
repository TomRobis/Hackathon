from socket import *
from termcolor import colored
from host import player_handler
import threading
import configuration
import time


def setup_game_host():
    """
    the server that connects to the clients is built.
    :return: socket: server socket that will connect to clients over tcp
    """
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', configuration.tcp_port))
    serverSocket.listen(1)
    return serverSocket


def start_game():
    """
    the server allocates a socket to accept clients into the game via tcp connection
    when the admission is over, the "acceptance socket" is closed and no more clients are admitted.
    once they are all allocated to one of two groups, the server announces the start of the game to
    all clients simultaneously
    """
    server_socket = setup_game_host()
    # event is a flag. when admission time is over, event flag is raised and all clients start the game.
    event = threading.Event()
    p_handler = player_handler.player_handler()  # a designated component manages every micro game with each client
    future = time.time() + configuration.wait_time
    player_threads = []
    while time.time() < future:  # admission to game is timed
        try:
            server_socket.settimeout(future - time.time())
            connectionSocket, addr = server_socket.accept()
            # player handler manages the game for the game host - assigns teams to groups and supervises the game
            t = threading.Thread(target=p_handler.handle_client, args=(connectionSocket, event))
            print(colored('a client has been received! hurray!', "magenta"))
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
