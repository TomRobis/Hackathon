import msvcrt


def listen_and_send(player_socket,game_status):
    while not game_status.is_game_over():
        try:
            if msvcrt.kbhit():
                c = msvcrt.getch()
                player_socket.send(c)
        except ConnectionResetError:
            print('server hung up on us')