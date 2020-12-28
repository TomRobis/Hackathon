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
    try:
        welcome_msg = clientSocket.recv(1024)
    except ConnectionResetError:
        print('Damn server hung up on us!')
        clientSocket.close()
        return
    print(welcome_msg.decode())
    boli = Boolen()
    keyboard = Virtual_keyboard(clientSocket)
    threading.Thread(target=keyboard.listen, args=(boli,)).start()
    end_game_msg = clientSocket.recv(1024)
    boli.set()
    print(end_game_msg.decode())
    clientSocket.close()
