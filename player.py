import concurrent
import threading

import game_functions.room_searcher, game_functions.game_player


def run_player():
    tcp_addr = game_functions.room_searcher.activate_server()
    for i in range(2):
        t = threading.Thread(target=game_functions.game_player.activate_server, args=(tcp_addr,))
        t.start()
