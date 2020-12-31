import threading
import client.game_room_searcher
import client.game_player
from client import game_player


def run_player():
    """
    the client performs two actions:
    1. they capture a udp packet containing the host's game server address.
    2. they use the address obtained to enter a game hosted by the server.
    """
    while 1:
        tcp_addr = client.game_room_searcher.connect_to_game_room()
        if tcp_addr[0] is not None:  # if the address is valid
            game_player.play_game(tcp_addr)


# is currently not in use.
# provides the ability to run multiple clients simultaneously
def run_threaded_players():
    """
    the client performs two actions:
    1. they capture a udp packet containing the host's game server address.
    2. they use the address obtained to enter a game hosted by the server.
    """
    while 1:
        tcp_addr = client.game_room_searcher.connect_to_game_room()
        t1 = threading.Thread(target=game_player.play_game, args=(tcp_addr,))
        t2 = threading.Thread(target=game_player.play_game, args=(tcp_addr,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
