from socket import *

from distlib.compat import raw_input


def activate_server(server_addr):
    team_name = 'Rocket'
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server_addr)
    team_assignment = team_name
    clientSocket.send(team_name.encode())
    # modifiedSentence = clientSocket.recv(1024)
    clientSocket.close()