import threading

from pip._vendor.colorama import init

import client.game_room_searcher, client.game_player
from client import game_player


def run_player():
    while 1:
        tcp_addr = client.game_room_searcher.connect_to_game_room()
        t1 = threading.Thread(target=game_player.play_game, args=(tcp_addr,))
        t2 = threading.Thread(target=game_player.play_game, args=(tcp_addr,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()