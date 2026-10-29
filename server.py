import socket 
import threading
from dotenv import load_dotenv

host = "0.0.0.0"
port = 4444

load_dotenv()

 


Clients = {}
lock = threading.Lock()


def broadcast(message:str, sender_sock = None):
    payload = (message +"\n").encode("utf-8")
    with lock:
        for c_sock in list(Clients.keys()):
            if c_sock != sender_sock and Clients[c_sock] is not None:
                try:
                    c_sock.sendall(payload)
                except Exception:
                    remove_client(c_sock)
def remove_client(c_sock):
    username = None 
    with lock:
        if c_sock in Clients:
            username = Clients.pop(c_sock)
            try:
                c_sock.close()
            except Exception:
                pass
    if username:
        broadcast(f"[->] {username} has left the Chat")
        print(f"[LEAVE] {username} disconnected")
def handle_client(sock,addr):
    with lock:
        Clients[sock] = None
    try:
        sock.sendall(
            b"[SYSTEM] COnnected Type '/join <username>' to enter the Chat.\n"
        )
        while True:
            data = sock.recv(1024)
            if not data:
                break

            text = data.decode("utf-8").strip()
            print(text)
            if not text:
                continue
            
            if text.startswith("/join"):
                split_text = text.split(" ", 1)
                if len(split_text) < 2 or not split_text[1].strip():
                    sock.sendall(b"[!] Usage : /join <username>\n")
                    continue

                requested_name = split_text[1].strip()

                with lock:
                    if Clients[sock] is not None:
                        sock.sendall(
                            f"[!] You are already joined as {Clients[sock]}.\n".encode("utf-8")
                        )
                        continue

                    if requested_name in Clients.values():
                        sock.sendall(b"[!] That username is taken. Pick another.\n")
                        continue

                    Clients[sock] = requested_name

                sock.sendall(
                    f"[<-] Joined successfully as {requested_name}. Use '/send <message>' to send message\n".encode("utf-8")
                )
                broadcast(f"[<-] {requested_name} joined the chat!", sender_sock=sock)
                print(f"[JOIN] {requested_name} registered from {addr}")

            elif text.startswith("/send"):
                with lock:
                    current_user = Clients.get(sock)

                if current_user is None:
                    sock.sendall(b"[!] You must use '/join <username>' first")
                    continue
                split_text = text.split(" ",1)
                if len(split_text) < 2 or not split_text[1].strip():
                    sock.sendall(b"[!] Usage: /send <message> \n")
                    continue
                message_body = split_text[1].strip()
                broadcast(f"[{current_user} : {message_body}]",sender_sock=sock)
                sock.sendall(b"[OK] Message send.\n")
            elif text.lower() == "/leave":
                sock.sendall(b"[SYSTEM] you left the chat.Good bye broo\n")
                break
            else:
                sock.sendall(
                    b"[!] Unknown Commend. Valid: /join <name> , /send <message> , /leave \n"
                )
    except (ConnectionResetError,ConnectionAbortedError):
        pass
    finally:
        remove_client(sock)
def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((host,port))
    server.listen(10)
    print("Chat server listening on {}-{}".format(host,port))

    try:
        while True:
            c_sock , c_addr = server.accept()

            t = threading.Thread(
                target=handle_client,
                args=(c_sock,c_addr),
                daemon=True,
            )
            t.start()

    except KeyboardInterrupt:
        print("\n Server shutting Down")
    finally:
        server.close()

def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((host,port))
    server.listen(10)
    print("Chat server listening on {}-{}".format(host,port))

    try:
        while True:
            c_sock , c_addr = server.accept()

            t = threading.Thread(
                target=handle_client,
                args=(c_sock,c_addr),
                daemon=True,
            )
            t.start()

    except KeyboardInterrupt:
        print("\n Server shutting Down")
    finally:
        server.close()
def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((host,port))
    server.listen(10)
    print("Chat server listening on {}-{}".format(host,port))

    try:
        while True:
            c_sock , c_addr = server.accept()

            t = threading.Thread(
                target=handle_client,
                args=(c_sock,c_addr),
                daemon=True,
            )
            t.start()

    except KeyboardInterrupt:
        print("\n Server shutting Down")
    finally:
        server.close()



if __name__ == "__main__":
    main()

