import threading
from socket import *
from termcolor import colored

import configuration
from client.keyboards import listener_keyboard, msvcrt_keyboard
from client.booli_is_back import booli_is_back


def play_game(server_addr):
    try:
        client_socket = connect_with_server(server_addr)
    except (ConnectionResetError, TimeoutError) as e:
        print(colored("Damn server doesn't let us in!","red"))
        return
    if register_team_to_group(client_socket):
        # pass
        send_chars(client_socket)
    client_socket.close()  # game over


def connect_with_server(server_address):
    print(colored("Received offer from " + server_address[0] + " , attempting to connect...", "blue"))
    team_name = configuration.team_name
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server_address)
    clientSocket.settimeout(configuration.wait_time * 2)
    clientSocket.send(team_name.encode())
    return clientSocket


def register_team_to_group(client_socket):
    try:
        welcome_msg = client_socket.recv(4096)
        print(colored(welcome_msg.decode(), "green"))
        return True
    except (ConnectionResetError, TimeoutError) as e:
        print(colored('Damn server hung up on us!', "red"))
        client_socket.close()
        return False


def send_chars(client_socket):
    vk = listener_keyboard.listener_keyboard(client_socket)
    t1 = threading.Thread(target=vk.listen_and_send)
    t1.start()
    try:
        end_game_msg = client_socket.recv(1024)
    except ConnectionResetError:
        print(colored('Damn server hung up on us!', 'red'))
        return
    print(colored(end_game_msg.decode(),"cyan"))

def send_chars_virtual_keyboard(client_socket):
    end_game_flag = booli_is_back()
    t1 = threading.Thread(target=msvcrt_keyboard.listen_and_send, args=(client_socket, end_game_flag,))
    t1.start()
    try:
        end_game_msg = client_socket.recv(1024)
        end_game_flag.end_game()
    except ConnectionResetError:
        print(colored('Damn server hung up on us!', 'red'))
        return
    print(colored(end_game_msg.decode(),"cyan"))