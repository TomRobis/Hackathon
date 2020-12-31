from threading import Thread

import host.game_host
import host.room_advertising
import pretty_print


def run_host():
    while True:
        t1 = Thread(target=host.game_host.start_game)  # tcp server
        t2 = Thread(target=host.room_advertising.broadcast_game_server_ip)  # udp that advertises tcp server port and ip
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(f"{pretty_print.pretty_print.WARNING}Game over, sending out offer requests...")
