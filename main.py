from threading import Thread

from pip._vendor.colorama import init

from host.host import run_host
from client.player import run_player

init()
# Thread(target = run_host).start()
Thread(target=run_player).start()
# def run_main():
#     init()
#     Thread(target = run_host).start()
#     Thread(target = run_player).start()
# if __name__ == '__main__':
#     run_main()
