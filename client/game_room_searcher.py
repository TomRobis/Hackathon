import struct
from socket import *
from termcolor import colored
import configuration


def set_udp_room_searcher():
    """
    the client's udp socket is built, in order to capture the TCP server's port to connect to later.
    :return: socket: udp socket that listens on a pre - designated port.
    """
    listener_port = configuration.broadcast_port
    listener_udp_socket = socket(AF_INET, SOCK_DGRAM)
    listener_udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listener_udp_socket.bind(('', listener_port))
    return listener_udp_socket


def validate_and_decode_message(message):
    """
    the client "unwraps" the udp message sent from the server, and authenticates it.
    authentication is done in two levels:
    1. magic cookie identifier and message type are validated, otherwise permission is denied
    - message is of wrong formatting.
    2. the port has to be in a certain range in order to be legitimate - otherwise it has a wrong value.
    :param message:
    :return: int / None:
     if the message is validated, the port of the tcp server currently waiting for clients(players)
     otherwise, if the message isn't validated,
    """
    try:
        encoded_msg = struct.unpack(configuration.broadcast_pack_unpack_format, message)
        decoded_message = [hex(encoded_msg[0]), hex(encoded_msg[1]), encoded_msg[2]]
        if str(decoded_message[0]) != '0x' + configuration.broadcast_magic_cookie_identifier:  # magic cookie identifier
            raise PermissionError("message doesn't start with magic cookie identifier. your mama is stupid.")
        elif str(decoded_message[1]) != '0x' + configuration.broadcast_message_type:  # message identifier
            raise PermissionError("message type not supported. your mama is stupid.")
        elif 0 >= decoded_message[2] or decoded_message[2] > 65535:  # port validation
            raise ValueError("port number isn't valid. your mama is stupid")
    except (ValueError, PermissionError):
        return None
    return int(decoded_message[2])  # data of message, port of the host's tcp server


def connect_to_game_room():
    """
    at this point, the client attempts to capture a tcp server's port to connect to.
    firstly, they establish a udp socket to capture packets that are sent with said information.
    secondly, a packet sent by a server is captured.
    thirdly, the information is unpacked and validated.
    finally, the socket is closed, and the client proceeds to connect to the sever over tcp and
    play a game they host.
    :return: str,int: full address of the tcp server of the host.
    """
    listener_udp_socket = set_udp_room_searcher()
    print(colored("Client started, listening for offer requests...", "yellow"))

    message, ip_port_tup = listener_udp_socket.recvfrom(configuration.udp_receiver_buffer_size)

    port_of_host_tcp_server = validate_and_decode_message(message)

    listener_udp_socket.close()

    return ip_port_tup[0], port_of_host_tcp_server
