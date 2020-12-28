import concurrent
import threading
import time

import game_functions.room_searcher,game_functions.game_player
def run_player():
    tcp_addr = game_functions.room_searcher.activate_server()
    threading.Thread(target=game_functions.game_player.activate_server,args=(tcp_addr,)).start()
    threading.Thread(target=game_functions.game_player.activate_server,args=(tcp_addr,)).start()

