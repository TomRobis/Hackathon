from socket import *

#sender
# class UDP_server:
def activate_server():
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
    clientSocket.sendto(bytes(magic_cookie + message_type + TCP_port,'utf-8'), (broadcast_address,clients_listening_port))