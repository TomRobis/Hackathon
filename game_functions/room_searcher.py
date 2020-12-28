import struct
from socket import *

from termcolor import colored


def activate_server():  # UDP client
    serverPort = 13117
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print(colored("Client started, listening for offer requests...", "yellow"))
    message, ip_port_tup = serverSocket.recvfrom(1024)  # buffer size
    encoded_msg = struct.unpack('!III', message)
    encoded_msg = [hex(encoded_msg[0]),hex(encoded_msg[1]),encoded_msg[2]]
    if str(encoded_msg[0]) != '0xfeedbeef':
        raise ValueError("message doesn't start with magic cookie identifier. your mama is stupid.")
    elif str(encoded_msg[1]) != '0x2':
        raise ValueError("message type not supported. your mama is stupid.")
    serverSocket.close()
    return ip_port_tup[0], int(encoded_msg[2])  # ip of game host and port of tcp server
