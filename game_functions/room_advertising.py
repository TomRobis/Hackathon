# sender
# class UDP_server:
import time
from socket import *

from termcolor import colored


def activate_server(ip_address):
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.bind(('', serverPort))
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # clients_address = "172.1.0.255"
    broadcast_address = "255.255.255.255"
    clients_listening_port = 13117
    magic_cookie = '0xfeedbeef'
    message_type = '0x2'
    TCP_port = '2112'
    print(colored("Server started,listening on IP address ", 'blue') + colored(ip_address, 'red'))
    future = time.time() + 10
    while future > time.time():
        clientSocket.sendto(bytes(magic_cookie + message_type + TCP_port, 'utf-8'),
                            (broadcast_address, clients_listening_port))
        time.sleep(1)
