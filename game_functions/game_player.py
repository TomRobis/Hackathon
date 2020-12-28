from socket import *

from termcolor import colored
from pynput.keyboard import Listener

def activate_server(server_addr):
    print(colored("Received offer from " + server_addr[0] + " , attempting to connect...", "blue"))
    team_name = 'Rocket'
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server_addr)
    clientSocket.send(team_name.encode())
    welcome_msg = clientSocket.recv(1024)
    print(welcome_msg.decode())
    # keyboard = virtual_keyboard.listen()
    while True:
        pass
        # with Listener(on_press=on_press,on_release=on_release) as listener:
        # clientSocket.send(keyboard.(Key.space).encode())
    clientSocket.close()
