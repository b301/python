"""
__author__ == "b301"
__version__ == "3.9.6"

Not the best ... but it kinda works?
"""

import threading
import socket


HOST = "0.0.0.0"
PORT = 20031
MEMBERS = {} # Member's sockets


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"SERVER::Listening on {HOST}:{PORT}")

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
            for member in MEMBERS:
                dc.append(member)
            for client in dc:
                stop_connection(client)
            exit(1)

    return None


def console(server_socket: socket.socket) -> None:
    """
    the server console
    """
    while True:
        cmd = input().lower()
        if cmd == "exit" or cmd == "shutdown":
            print("Server is shutting down.")
            server_socket.close()
        elif cmd == "help":
            print("Enter `EXIT` or `SHUTDOWN` to stop the server.")
        else:
            print(f"Invalid command: {cmd} .. type HELP for list of available commands.")

    return


def member_handler(member: socket.socket) -> None:
    """
    responsible for handling the messages being sent and received
    """
    while True:
        m = member.recv(1024).decode('utf-8')
        if m.lower() == f"{MEMBERS[member]}: exit":
            stop_connection(member)
            break
        broadcast(m, source=members[member])

    return


def stop_connection(member: socket.socket) -> None:
    """
    terminates connection with a member
    """
    member.close()
    gone = MEMBERS[member]
    MEMBERS.pop(member, members[member])
    broadcast(f"{gone} disconnected.")
    
    return


def broadcast(message: str, source="SERVER") -> None:
    """
    sends a message to all connected members
    """
    print(f"{source}: {message}")
    for member in MEMBERS.keys():
        member.send(f"{source}: {message}".encode('utf-8'))

    return


if __name__ == "__main__":
    main()
