import struct
import time
from socket import *
from termcolor import colored

import configuration


def setup_udp_room_broadcaster():
    serverPort = configuration.udp_port
    room_broadcaster = socket(AF_INET, SOCK_DGRAM)
    room_broadcaster.setsockopt(SOL_SOCKET,  SO_REUSEADDR, 1)
    room_broadcaster.bind(('', serverPort))
    room_broadcaster.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    return room_broadcaster


def make_msg():
    magic_cookie = int('feedbeef', 16)
    message_type = int('2', 16)
    TCP_port = int(configuration.tcp_port)
    return struct.pack('>Ibh', magic_cookie, message_type, TCP_port)


def send_game_host_ip(msg, room_broadcaster_socket):
    broadcast_address = configuration.broadcast_addr
    players_broadcast_port = configuration.broadcast_port
    future = time.time() + configuration.wait_time
    # UDP server and TCP server might be in different computers
    print(colored("Server started,listening on IP address ", 'blue') + colored(configuration.local_ip_addr, 'red'))
    while future > time.time():
        room_broadcaster_socket.sendto(msg, (broadcast_address, players_broadcast_port))
        time.sleep(1)


def broadcast_game_server_ip():
    room_broadcaster_socket = setup_udp_room_broadcaster()
    msg = make_msg()  # wrap the message with a magic cookie identifier and certain message type
    send_game_host_ip(msg, room_broadcaster_socket)
    room_broadcaster_socket.close()
