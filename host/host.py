from threading import Thread

from termcolor import colored

import host.game_host
import host.room_advertising


def run_host():
    while 1:
        t1 = Thread(target=host.game_host.start_game)  # tcp server
        t2 = Thread(target=host.room_advertising.broadcast_game_server_ip)  # udp that advertises tcp server port and ip
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(colored("Game over, sending out offer requests...","magenta"))
