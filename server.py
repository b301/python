"""
__author__ == "b301"
__version__ == "3.9.6"

Not the best ... but it kinda works?
"""

import threading
import socket


host = "127.0.0.1"
port = 20031
members = {} # Member's sockets

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print("SERVER::Listening")

    console_thread = threading.Thread(target=console, args=(server, ), daemon=True)
    console_thread.start()

    while True:
        try:
            member, address = server.accept()
            print(f"SERVER::Connected to {str(address)}")
            nickname = member.recv(1024).decode("utf-8")
            
            members[member] = nickname
            member.send("Server::Connected to the server".encode("utf-8"))
            broadcast(f"Connected to the server")

            member_thread = threading.Thread(target=member_handler, args=(member, ), daemon=True)
            member_thread.start()
        except OSError as e:
            print(f"SERVER::Exiting, Exception: {e}")
            dc = []
            for member in members:
                dc.append(member)
            for s in dc:
                stop_connection(s)
            exit(1)

def console(server_socket: socket.socket):
    while True:
        cmd = input().lower()
        if cmd == "exit":
            server_socket.close()

def member_handler(member: socket.socket):
    """
    responsible for handling the messages being sent and received
    """
    while True:
        m = member.recv(1024).decode('utf-8')
        if m.lower() == f"{members[member]}: exit":
            stop_connection(member)
            break
        broadcast(m, source=members[member])

    return

def stop_connection(member: socket.socket):
    """
    terminates connection with a member
    """
    member.close()
    gone = members[member]
    members.pop(member, members[member])
    broadcast(f"{gone} disconnected.")
    
    return

def broadcast(message: str, source="SERVER"):
    """
    sends a message to all connected members
    """
    for member in members.keys():
        print(f"{source}: {message}")
        member.send(f"{source}: {message}".encode('utf-8'))

    return


if __name__ == "__main__":
    main()