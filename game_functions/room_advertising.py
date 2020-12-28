# sender
# class UDP_server:
import struct
import time
from socket import *

from termcolor import colored


def activate_server(ip_address):
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.bind(('', serverPort))
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    magic_cookie = int('feedbeef', 16)
    message_type = int('2', 16)
    # broadcast_address = "172.1.0.255"
    broadcast_address = "255.255.255.255"
    TCP_port = int(2112)
    msg = struct.pack('!III', magic_cookie, message_type, TCP_port)
    clients_listening_port = 13117
    future = time.time() + 10
    print(colored("Server started,listening on IP address ", 'blue') + colored(ip_address, 'red'))
    while future > time.time():
        clientSocket.sendto(msg, (broadcast_address, clients_listening_port))
        time.sleep(1)
