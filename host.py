from threading import Thread

import game_functions.room_advertising,game_functions.game_host
import socket


def run_host():
    while(1):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        t1 = Thread(target=game_functions.game_host.activate_server) #tcp server
        t2 = Thread(target=game_functions.room_advertising.activate_server, args=(IPAddr,)) #udp that advertises tcp server port and ip
        t1.start()
        t2.start()
        t1.join()
        t2.join()

