from concurrent.futures.thread import ThreadPoolExecutor
from socket import *
from threading import Thread

from game_functions import player_handler
import time


def activate_server():
    serverPort = 2112
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)

    p_handler = player_handler.player_handler()
    future = time.time() + 10
    num_of_threads = 5
    executor = ThreadPoolExecutor(num_of_threads)
    while time.time() < future:  # time out
        try:
            serverSocket.settimeout(future - time.time()) # time left
            connectionSocket, addr = serverSocket.accept()
            executor.submit(p_handler.handle_client(connectionSocket))
        except:
            print('recieve window is closed')
            break
    executor.shutdown()  # finish dividing into teams
    print('mefanek kaze, print tov')
    serverSocket.close()
