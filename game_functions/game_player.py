from socket import *

from distlib.compat import raw_input
from termcolor import colored


def activate_server(server_addr):
    print(colored("Received offer from " + server_addr[0] + " , attempting to connect...", "blue"))
    team_name = 'Rocket'
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server_addr)
    team_assignment = team_name
    clientSocket.send(team_name.encode())
    # modifiedSentence = clientSocket.recv(1024)
    clientSocket.close()
