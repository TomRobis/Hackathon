import struct
import time
from socket import *
from termcolor import colored


def setup_udp_room_broadcaster():
    serverPort = 12000
    room_broadcaster = socket(AF_INET, SOCK_DGRAM)
    room_broadcaster.bind(('', serverPort))
    room_broadcaster.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    return room_broadcaster


def make_msg():
    magic_cookie = int('feedbeef', 16)
    message_type = int('2', 16)
    TCP_port = int(2112)
    return struct.pack('!III', magic_cookie, message_type, TCP_port)


def send_game_host_ip(msg, room_broadcaster_socket,ip_address):
    broadcast_address = "255.255.255.255"
    # broadcast_address = "172.1.0.255"
    players_broadcast_port = 13117
    future = time.time() + 10
    # UDP server and TCP server might be in different computers
    print(colored("Server started,listening on IP address ", 'blue') + colored(ip_address, 'red'))
    while future > time.time():
        room_broadcaster_socket.sendto(msg, (broadcast_address, players_broadcast_port))
        time.sleep(1)


def broadcast_game_server_ip(ip_address):
    room_broadcaster_socket = setup_udp_room_broadcaster()
    msg = make_msg() # wrap the message with a magic cookie identifier and certain message type
    send_game_host_ip(msg, room_broadcaster_socket,ip_address)
