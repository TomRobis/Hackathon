from socket import *
from termcolor import colored
from client.keyboards import listener_keyboard
import threading
import configuration

# from client.booli_is_back import booli_is_back
# from client.keyboards import msvcrt_keyboard


def play_game(server_addr):
    """
    as soon as a TCP address of the server is obtained, the client is sent to this function to make all the
    necessary steps to start a game with a server:
    1. connect to it
    2. allow it to assign the team name to a group of its' choice
    3. play the game (capture keyboard clicks and send them to the server over the tcp connection)
    finally, the client closes the connection.

    :param server_addr: the TCP server's address to connect to.
    """
    try:
        client_socket = connect_with_server(server_addr)
    except (ConnectionResetError, TimeoutError):  # in case the connection doesn't succeed
        print(colored("Damn server doesn't let us in!", "red"))
        return  # the client exits and searches for a different server to connect to
    if register_team_to_group(client_socket):
        send_chars(client_socket)
    client_socket.close()  # game over


def connect_with_server(server_address):
    """
    the client connects with the server over tcp connection, using the server address sent over the udp broadcast
    if the connection doesn't succeed, it is caught at the handler - "play_game"

    :param server_address::param server_addr: the TCP server's address to connect to.
    :return: the socket that connects to the server over tcp - the client's socket.
    """
    print(colored("Received offer from " + server_address[0] + " , attempting to connect...", "blue"))
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server_address)
    clientSocket.settimeout(configuration.wait_time * 2)
    clientSocket.send(configuration.team_name.encode())
    return clientSocket


def register_team_to_group(client_socket):
    """
    once a client has established a connection to the server, they wait until a message is sent to
    them by the server, letting them know the game has begun.
    :param client_socket: the socket on the client's side that is already connected to the server.
    :return: boolean - the client specifies whether the message has been received as expected,
    which is later caught by the handler - "play_game"
    """
    try:
        welcome_msg = client_socket.recv(configuration.standard_buffer_size)
        print(colored(welcome_msg.decode(), "green"))
        return True
    except (ConnectionResetError, TimeoutError):  # in case the message wasn't received as planned
        print(colored('Damn server hung up on us!', "red"))
        client_socket.close()  # the socket is closed and client resumes to look for a new server to connect to.
        return False


def send_chars(client_socket):
    """
    the client has started the game!
    they are required to send capture keyboard presses made by the user and send them to the server.
    the server, in turn, documents the presses sent to it to the group which was assigned to the client.
    once the game is done, a message is sent to the client that announces the winners.
    :param client_socket: the socket on the client's side that is already connected to the server.
    """

    # a designated class that captures keyboard presses
    keyboard_presses_listener = listener_keyboard.listener_keyboard(client_socket)
    t1 = threading.Thread(target=keyboard_presses_listener.listen_and_send)
    t1.start()
    try:  # the client waits for the end game message while the game is played.
        end_game_msg = client_socket.recv(configuration.standard_buffer_size)

    # if the server disconnects, the client proceeds to look for a new game in a new server.
    except ConnectionResetError:
        print(colored('Damn server hung up on us!', 'red'))
        return
    print(colored(end_game_msg.decode(), "cyan"))


# is currently not in use.

# def send_chars_virtual_keyboard(client_socket):
#     """
#     the client has started the game!
#     they are required to send capture keyboard presses made by the user and send them to the server.
#     the server, in turn, documents the presses sent to it to the group which was assigned to the client.
#     once the game is done, a message is sent to the client that announces the winners.
#     :param client_socket: the socket on the client's side that is already connected to the server.
#     """
#     end_game_flag = booli_is_back()
#     t1 = threading.Thread(target=msvcrt_keyboard.listen_and_send, args=(client_socket, end_game_flag,))
#     t1.start()
#     try:
#         end_game_msg = client_socket.recv(configuration.standard_buffer_size)
#         end_game_flag.end_game()
#     except ConnectionResetError:
#         print(colored('Damn server hung up on us!', 'red'))
#         return
#     print(colored(end_game_msg.decode(), "cyan"))
