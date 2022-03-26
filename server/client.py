"""
__author__ == "b301"
__python__ == "3.9.6"
__version__ == "0.2"

Not the best ... but it works?
"""


import threading
import socket
import time


HOST = "1.2.3.4"
PORT = 20031


nickname = input("Choose a nickname: ")


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send(nickname.encode('utf-8'))

    receive_thread = threading.Thread(target=recieve, args=(client, ), daemon=True)
    receive_thread.start()

    send(client)


def recieve(client: socket.socket):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
            if  (
                message == f"[Server]: The nickname {nickname} is taken." or
                message == "[Server]: Shutting down." or
                message == "[Server]: You have been kicked"
                ):
                return
            elif message == "[Server]: Goodbye.":
                client.close()
                return
        except Exception as e:
            client.close()
            return


def send(client: socket.socket):
    while True:
        try:
            message = input()
            client.send(message.encode("utf-8"))
            if message.lower() == "exit":
                return
        except WindowsError as e:
            if e.winerror == 10054:
                print("Exiting...")
                return
        except Exception as e:
            print(f"Exception raised: {e}")
            return


if __name__ == "__main__":
    main()
