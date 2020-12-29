import threading

import client.game_room_searcher, client.game_player
import game_player_test


def run_player():
    while 1:
        tcp_addr = client.game_room_searcher.connect_to_game_room()
        # t1 = threading.Thread(target=client.game_player.play_game, args=(tcp_addr,))
        # t2 = threading.Thread(target=client.game_player.play_game, args=(tcp_addr,))
        t1 = threading.Thread(target=game_player_test.play_game, args=(tcp_addr,))
        t2 = threading.Thread(target=game_player_test.play_game, args=(tcp_addr,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()