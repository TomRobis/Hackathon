import threading
import time
from socket import *

from termcolor import colored

from game_functions.Boolen import Boolen
from game_functions.virtual_keyboard import Virtual_keyboard


def activate_server(server_addr):
    print(colored("Received offer from " + server_addr[0] + " , attempting to connect...", "blue"))
    team_name = 'Rocket'
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server_addr)
    clientSocket.send(team_name.encode())
    welcome_msg = clientSocket.recv(1024)
    print(welcome_msg.decode())
    boli = Boolen()
    keyboard = Virtual_keyboard(clientSocket)
    threading.Thread(target=keyboard.listen, args=(boli,)).start()
    time.sleep(5)
    boli.set()
    clientSocket.close()
