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
LOG_MESSAGES = True


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
            
            if nickname in MEMBERS.values():
                member.send(f"[Server]: The nickname {nickname} is taken.".encode('utf-8'))
                stop_connection(member)

            else:
                MEMBERS[member] = nickname
                member.send("[Server]: Connected to the server.".encode("utf-8"))
                broadcast(f"[*] {nickname} connected to the server.")

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

    return


def console(server_socket: socket.socket) -> None:
    """
    the server console
    """
    while True:
        cmd = input().lower()
        print('\r')
        if cmd == "exit" or cmd == "shutdown":
            print("Server is shutting down.")
            server_socket.close()
        elif cmd == "help":
            print("[Server-Console]:\n\tEnter `EXIT` or `SHUTDOWN` to stop the server.\
                \n\tEnter `BROADCAST` to broadcast a message.\n\tEnter `DISCONNECT` to disconnect a member.\
                \n\tEnter `MEMBER LIST` to view the member list.")
        elif cmd == "broadcast":
            bc = input("[Server-Console]: message (type `abort` to abort): ")
            if bc == "abort":
                print("[Server-Console]: Aborted broadcast.")
            elif bc != '':
                broadcast(message=bc, source="SERVER")
        elif cmd == "disconnect":
            member_name = input("[Server-Console]: Who would you like to disconnect? ")
            if member_name in MEMBERS.values():
                stop_connection(
                    list(MEMBERS.keys())[list(MEMBERS.values()).index(member_name)]
                    )
            else:
                print(f"[Server-Console]: {member_name} is not in members.")
        elif cmd == "member list":
            print("\n\tMembers:")
            for member in MEMBERS.values():
                print(f"\t\t{member}")
        else:
            print(f"[Server-Console]: Invalid command: `{cmd}` ... type HELP for list of available commands.")

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
        broadcast(m, source=MEMBERS[member])

    return


def stop_connection(member: socket.socket) -> None:
    """
    terminates the connection with a member
    """
    member.close()
    dc_member = MEMBERS[member]
    MEMBERS.pop(member, MEMBERS[member])
    broadcast(f"[!] {dc_member} disconnected.")
    
    return


def broadcast(message: str, source="SERVER") -> None:
    """
    sends a message to all connected members
    """
    if LOG_MESSAGES:
        with open("logs.txt", 'a') as f:
            f.write(f"[{source}]: {message}\n")
    print(f"[{source}]: {message}")
    for member in MEMBERS.keys():
        if member != source:
            member.send(f"[{source}]: {message}".encode('utf-8'))

    return


if __name__ == "__main__":
    main()
