import threading
from socket import *

from pip._vendor.colorama import init
from termcolor import colored

from client.virtual_keyboard import virtual_keyboard


def play_game(server_addr):
    client_socket = connect_with_server(server_addr)
    if register_team_to_group(client_socket):
        # send_chars(client_socket)
        pass
    client_socket.close()  # game over


def connect_with_server(server_address):
    print(colored("Received offer from " + server_address[0] + " , attempting to connect...", "blue"))
    team_name = 'RedHatYossi\n'
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server_address)
    clientSocket.send(team_name.encode())
    return clientSocket


def register_team_to_group(client_socket):
    try:
        welcome_msg = client_socket.recv(4096)
        print(colored(welcome_msg.decode(), "green"))
        return True
    except ConnectionResetError:
        print(colored('Damn server hung up on us!', "red"))
        client_socket.close()
        return False


def send_chars(client_socket):
    keyboard = virtual_keyboard(client_socket)
    threading.Thread(target=keyboard.listen).start()
    end_game_msg = client_socket.recv(1024)
    print(end_game_msg.decode())
