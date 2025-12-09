import socket
import threading

def listen(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode(), end="")
        except:
            break


def main():
    ip = input("Введите IP сервера: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 9090))

    threading.Thread(target=listen, args=(sock,), daemon=True).start()

    while True:
        msg = input()
        sock.send(msg.encode())


if __name__ == "__main__":
    main()
