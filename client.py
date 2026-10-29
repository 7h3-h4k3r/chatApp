import socket 
import threading
from dotenv import load_dotenv
import sys
host = "0.0.0.0"
port = 4444

load_dotenv()

try:
    import dotenv
    import os
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
except:
    pass

def receive_listener(sock):
    while True:
        try:
            data = sock.recv(2048)
            if not data:
                print("\n[!] Connection closed by server")
                break
            print(data.decode("utf-8",errors="ignore"),end="",flush=True)
        except (ConnectionResetError, OSError):
            break

def  main():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.connect((host,port))
    except ConnectionRefusedError:
        print("[!] Unable to connect to the chat server at {} - {}".format(host,port))
        sys.exit(1)
    threading.Thread(target=receive_listener, args=(sock,),daemon=True).start()

    try:
        while True:
            cmd = input()
            if not cmd.strip():
                continue
            sock.sendall((cmd+" \n").encode("utf-8"))
            if cmd.strip().lower() == "/leave":
                break
    except (KeyboardInterrupt,EOFError):
        sock.sendall(b"/leave\n")
    finally:
        sock.close()
        print("[*] Exited Client.")
if __name__ == "__main__":
    main()
