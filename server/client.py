"""
__author__ == "b301"
__version__ == "3.9.6"
"""

import threading
import socket


host = "127.0.0.1"
port = 20031

def main():
    nickname = input("Choose a nickname: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(nickname.encode('utf-8'))
    
    receive_thread = threading.Thread(target=recieve, args=(client, ), daemon=True)
    receive_thread.start()

    send(client, nickname)

def recieve(client: socket.socket):
    while True:
        try:
            m = client.recv(1024).decode('utf-8')
            print(m)
        
        except Exception as e:
            print(f"ERROR::Terminating connection .. {e}")
            client.close()
            exit(1)

def send(client: socket.socket, nickname: str):
    while True:
        message = input()
        if message != '':
            client.send(message.encode("utf-8"))
            if message.lower() == "exit":
                exit()

if __name__ == "__main__":
    main()
