"""
__author__ == "b301"
__python__ == "3.9.6"
__version == "0.2"

Not the best ... but it works?
"""


import threading
import socket
import time
import sys
import os


HOST = "0.0.0.0"
PORT = 20031
MEMBERS = {}
LOG_MESSAGES = True


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[Server]: Listening on {HOST}:{PORT}")

    console_thread = threading.Thread(target=console, args=(server, ), daemon=True)
    console_thread.start()

    while True:
        try:
            member, address = server.accept()
            print(f"[Server]: Connected to {str(address)}")
            nickname = member.recv(1024).decode("utf-8")
            
            if nickname in MEMBERS.values():
                member.send(f"[Server]: The nickname {nickname} is taken.".encode('utf-8'))
                stop_connection(member)

            else:
                MEMBERS[member] = nickname
                member.send("[Server]: Connected to the server.".encode("utf-8"))
                broadcast(f"[!] {nickname} connected to the server.")

                member_thread = threading.Thread(target=member_handler, args=(member, ), daemon=True)
                member_thread.start()

        except OSError:
            print(f"[Server]: Shutting down.")
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
        if cmd == '':
            pass
        elif cmd == "exit" or cmd == "shutdown":
            print("[Server]: Shutdown started...")
            for member in MEMBERS:
                member.send("[Server]: Shutting down.".encode('utf-8'))
            members = list(MEMBERS.keys())
            for sock in members:
                stop_connection(sock)
            while True:
                if MEMBERS == {}:
                    server_socket.close()
                    break
            print("[Server]: Shutdown finished.")
        elif cmd == "help":
            print("[Server-Console]:\n\tEnter `EXIT` or `SHUTDOWN` to stop the server.\
                \n\tEnter `BROADCAST` to broadcast a message.\n\tEnter `DISCONNECT` to disconnect a member.\
                \n\tEnter `LIST MEMBERS` to view the member list.\n\tEnter `CLEAR` to clear the console.")
        elif cmd == "broadcast":
            bc = input("[Server-Console]: message (type `abort` to abort): ")
            if bc == "abort":
                print("[Server-Console]: Aborted broadcast.")
            elif bc != '':
                broadcast(message=bc, source="SERVER")
        elif cmd == "disconnect":
            member_name = input("[Server-Console]: Who would you like to disconnect? (Case-Sensitive): ")
            if member_name in MEMBERS.values():
                member_socket = list(MEMBERS.keys())[list(MEMBERS.values()).index(member_name)]
                member_socket.send("[Server]: You have been kicked".encode('utf-8'))
                time.sleep(0.5)
                stop_connection(member_socket)
            else:
                print(f"[Server-Console]: {member_name} is not in the members list.")
        elif cmd == "list members":
            print("\n\tMembers:")
            for member in MEMBERS.values():
                print(f"\t\t{member}")
        elif cmd == "clear":
            if sys.platform == "linux":
                os.system("clear")
            elif sys.platform == "win32":
                os.system("cls") 
        else:
            print(f"[Server-Console]: Invalid command: `{cmd}` ... type HELP for list of available commands.")

    return


def member_handler(member: socket.socket) -> None:
    """
    responsible for handling the messages being sent and received
    """
    while True:
        try:
            m = member.recv(1024).decode('utf-8')
            if m.lower() == f"exit":
                stop_connection(member)
                break
            broadcast(m, source=MEMBERS[member])
        except ConnectionAbortedError:
            break

    return


def stop_connection(member: socket.socket) -> None:
    """
    terminates the connection with a member
    """
    member.close()
    dc_member = MEMBERS[member]
    MEMBERS.pop(member, MEMBERS[member])
    time.sleep(0.5)
    broadcast(f"[!] {dc_member} disconnected.")
    
    return


def broadcast(message: str, source="Server") -> None:
    """
    sends a message to all connected members
    """
    if message.encode('utf-8') == '':
        return
    if LOG_MESSAGES:
        with open("logs.txt", 'a') as f:
            f.write(f"[{time.strftime('%d.%m.%Y %H:%M:%S')}] [{source}]: {message}\n")
    print(f"[{source}]: {message}")
    for member in MEMBERS.keys():
        if member != source:
            member.send(f"[{source}]: {message}".encode('utf-8'))

    return


if __name__ == "__main__":
    main()
