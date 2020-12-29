import struct
from socket import *

from termcolor import colored


def set_udp_room_searcher():
    listener_port = 13117
    listener_udp_socket = socket(AF_INET, SOCK_DGRAM)
    listener_udp_socket.bind(('', listener_port))
    return listener_udp_socket


def validate_and_decode_message(message):
    encoded_msg = struct.unpack('!III', message)  # unwrap to cookie, message type and data
    decoded_message = [hex(encoded_msg[0]), hex(encoded_msg[1]), encoded_msg[2]]  # decode cookie and msg type
    if str(decoded_message[0]) != '0xfeedbeef':  # magic cookie identifier
        raise ValueError("message doesn't start with magic cookie identifier. your mama is stupid.")  # todo change
    elif str(decoded_message[1]) != '0x2':  # message identifier
        raise ValueError("message type not supported. your mama is stupid.")  # todo change
    return int(decoded_message[2])  # data of message, port of the host's tcp server


def connect_to_game_room():
    listener_udp_socket = set_udp_room_searcher()
    print(colored("Client started, listening for offer requests...", "yellow"))

    # player receives ip of host and port of tcp server set up by host
    message, ip_port_tup = listener_udp_socket.recvfrom(1024)

    #  message should be decoded and checked for correctness
    port_of_host_tcp_server = validate_and_decode_message(message)

    # listening is over, ip of host's tcp server is obtained
    listener_udp_socket.close()

    return ip_port_tup[0], port_of_host_tcp_server  # ip of game host and port of tcp server
