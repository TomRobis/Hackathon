from threading import Thread

import host.room_advertising, host.game_host
import socket


def run_host():
    while(1):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        t1 = Thread(target=host.game_host.start_game) #tcp server
        t2 = Thread(target=host.room_advertising.broadcast_game_server_ip, args=(IPAddr,)) #udp that advertises tcp server port and ip
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Game over, sending out offer requests...")




