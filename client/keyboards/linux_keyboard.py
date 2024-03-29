import select
import tty
import sys
import termios


def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])  # was originally timeout=0


def listen_and_send(client_socket, end_game_flag):
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        while not end_game_flag.is_game_over():
            if isData():
                c = sys.stdin.read(1)[0]
                client_socket.send(c.encode())
    except ConnectionResetError:
        print('damn server hung up on us!')
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)