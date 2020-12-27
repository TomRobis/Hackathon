from threading import Thread

import game_functions.room_advertising,game_functions.game_host
import socket


def run_host():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    Thread(target=game_functions.game_host.activate_server).start() #tcp server
    Thread(target=game_functions.room_advertising.activate_server, args=(IPAddr,)).start() #udp that advertises tcp server port and ip
