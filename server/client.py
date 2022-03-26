"""
__author__ == "b301"
__python__ == "3.9.6"
__version__ == "0.2"

Not the best ... but it works?
"""


import threading
import socket
import time


HOST = "10.100.102.31"
PORT = 20031


nickname = input("[*] Choose a nickname: ")


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send(nickname.encode('utf-8'))

    receive_thread = threading.Thread(target=recieve, args=(client, ), daemon=True)
    receive_thread.start()

    send(client, nickname)


def recieve(client: socket.socket):
    while True:
        try:
            m = client.recv(1024).decode('utf-8')
            if m == f"[Server]: The nickname {nickname} is taken.":
                exit(0)
            else:
                print(m)
        except Exception as e:
            print(f"[ERROR]: Terminating connection .. {e}")
            client.close()
            exit(1)


def send(client: socket.socket, nickname: str):
    while True:
        message = input()
        if message != '':
            client.send(message.encode("utf-8"))
            if message.lower() == "exit":
                exit(0)


if __name__ == "__main__":
    main()
