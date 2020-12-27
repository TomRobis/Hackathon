from threading import Thread

import game_functions.room_advertising,game_functions.game_host

def run_host():
    Thread(target=game_functions.game_host.activate_server).start() #tcp server
    Thread(target=game_functions.room_advertising.activate_server).start() #udp that advertises tcp server port and ip
