import struct
from socket import *

from pip._vendor.colorama import init
from termcolor import colored

import configuration


def set_udp_room_searcher():
    listener_port = configuration.broadcast_port
    listener_udp_socket = socket(AF_INET, SOCK_DGRAM)
    listener_udp_socket.setsockopt(SOL_SOCKET,  SO_REUSEADDR, 1)
    listener_udp_socket.bind(('', listener_port))
    return listener_udp_socket


def validate_and_decode_message(message): #todo changed just now
    try:
        encoded_msg = struct.unpack('>IbH', message)  # unwrap to cookie, message type and data - total of 7 bytes
        decoded_message = [hex(encoded_msg[0]), hex(encoded_msg[1]), encoded_msg[2]]  # decode cookie and msg type
        if str(decoded_message[0]) != '0xfeedbeef':  # magic cookie identifier
            raise PermissionError("message doesn't start with magic cookie identifier. your mama is stupid.")
        elif str(decoded_message[1]) != '0x2':  # message identifier
            raise PermissionError("message type not supported. your mama is stupid.")
        elif 0 >= decoded_message[2] or decoded_message[2] > 65535:
            raise ValueError("port number isn't valid. your mama is stupid")
    except (ValueError,PermissionError) as e:
        return None
    return int(decoded_message[2])  # data of message, port of the host's tcp server


def connect_to_game_room():
    listener_udp_socket = set_udp_room_searcher()
    print(colored("Client started, listening for offer requests...", "yellow"))

    # player receives ip of host and port of tcp server set up by host
    message, ip_port_tup = listener_udp_socket.recvfrom(7)

    #  message should be decoded and checked for correctness
    port_of_host_tcp_server = validate_and_decode_message(message)

    # listening is over, ip of host's tcp server is obtained
    listener_udp_socket.close()

    return ip_port_tup[0], port_of_host_tcp_server  # ip of game host and port of tcp server
