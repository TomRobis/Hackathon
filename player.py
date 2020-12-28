import concurrent
import threading

import game_functions.room_searcher, game_functions.game_player


def run_player():
    while 1:
        tcp_addr = game_functions.room_searcher.activate_server()
        t1 = threading.Thread(target=game_functions.game_player.activate_server, args=(tcp_addr,))
        t2 = threading.Thread(target=game_functions.game_player.activate_server, args=(tcp_addr,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()