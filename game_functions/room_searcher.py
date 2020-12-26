from socket import *


def activate_server():  # UDP client
    serverPort = 13117
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    # serverSocket.settimeout(100000) #10 minutes
    while 1:
        message, ip_port_tup = serverSocket.recvfrom(1024)  # buffer size
        encoded_msg = str(message, 'utf-8')
        if not encoded_msg.startswith('0xfeedbeef'):
            raise ValueError("message doesn't start with magic cookie identifier. your mama is stupid.")
        elif not encoded_msg.replace('0xfeedbeef', '').startswith('0x2'):
            raise ValueError("message type not supported. your mama is stupid.")
        encoded_msg = encoded_msg.replace('0xfeedbeef0x2', '')
        print(encoded_msg)  # test
        break
    serverSocket.close()
    return ip_port_tup[0], int(encoded_msg)  # ip of game host and port of tcp server
