import concurrent
import threading

import game_functions.room_searcher,game_functions.game_player
def run_player():
    tcp_addr = game_functions.room_searcher.activate_server()
    threading.Thread(game_functions.game_player.activate_server(tcp_addr)).start()
    threading.Thread(game_functions.game_player.activate_server(tcp_addr)).start()

