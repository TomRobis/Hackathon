import struct
import time
from socket import *
from termcolor import colored

import configuration


def setup_udp_room_broadcaster():
    """
    the socket that broadcasts the game host's address is established
    :return: socket: said socket.
    """
    room_broadcaster = socket(AF_INET, SOCK_DGRAM)
    room_broadcaster.setsockopt(SOL_SOCKET,  SO_REUSEADDR, 1)
    room_broadcaster.bind(('', configuration.udp_port))
    room_broadcaster.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    return room_broadcaster


def make_msg():
    """
    the message broadcast to all potential game players is packed using a specific pre - instructed
    format, consisting of three fields:
    1. magic cookie identifier - pre - determined with players catpuring the broadcast
    2. message type - pre - determined with players catpuring the broadcast
    3. TCP_port - the port the game host is listening to
    :return: struct obj - said message
    """
    magic_cookie = int(configuration.broadcast_magic_cookie_identifier, configuration.hex_basis)
    message_type = int(configuration.broadcast_message_type, configuration.hex_basis)
    TCP_port = int(configuration.tcp_port)
    return struct.pack(configuration.broadcast_pack_unpack_format, magic_cookie, message_type, TCP_port)


def send_game_host_ip(msg, room_broadcaster_socket):
    """
    a broadcast is sent to all potential game players containing the game host's server's port.
    the broadcast is sent every 'broad_delay_message' time.
    :param msg: str: said message.
    :param room_broadcaster_socket: socket: a udp socket that broadcasts said message as depicted.
    """
    future = time.time() + configuration.wait_time
    # UDP server and TCP server might be in different computers
    print(colored("Server started,listening on IP address ", 'blue') + colored(configuration.local_ip_addr, 'red'))
    while future > time.time():
        room_broadcaster_socket.sendto(msg, (configuration.broadcast_addr, configuration.broadcast_port))
        time.sleep(configuration.broadcast_message_delay)


def broadcast_game_server_ip():
    """
    the host establishes a udp socket that broadcasts the game host's tcp server's port.
    potential players decypher the message and connect to it.
    """
    room_broadcaster_socket = setup_udp_room_broadcaster()
    msg = make_msg()  # wrap the message with a magic cookie identifier and certain message type
    send_game_host_ip(msg, room_broadcaster_socket)
    room_broadcaster_socket.close()
