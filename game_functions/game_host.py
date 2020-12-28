import threading
from concurrent.futures.thread import ThreadPoolExecutor
from socket import *
from threading import Thread

from game_functions import player_handler
import time


def activate_server():
    event = threading.Event()
    serverPort = 2112
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)

    p_handler = player_handler.player_handler()
    future = time.time() + 10
    while time.time() < future:  # time out
        try:
            serverSocket.settimeout(future - time.time())  # time left
            connectionSocket, addr = serverSocket.accept()
            threading.Thread(target=p_handler.handle_client, args=(connectionSocket, event)).start()
        except:
            print('recieve window is closed')
            break
    event.set()
    print('mefanek kaze, print tov')
    serverSocket.close()
