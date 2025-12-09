import socket
import threading

clients = {}

def handle_client(conn, addr):
    global clients

    conn.send("Введите ваше имя: ".encode())
    username = conn.recv(1024).decode().strip()

    clients[username] = conn
    print(f"[+] {username} подключился")

    broadcast(f"*** {username} вошёл в чат ***", username)

    try:
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            msg = msg.decode()

            if ":" not in msg:
                conn.send("Неверный формат. Используйте: получатель: сообщение\n".encode())
                continue

            receiver, text = msg.split(":", 1)
            receiver = receiver.strip()
            text = text.strip()

            if receiver not in clients:
                conn.send("Такого пользователя нет.\n".encode())
                continue

            clients[receiver].send(f"[{username}]: {text}\n".encode())

    except:
        pass
    finally:
        conn.close()
        del clients[username]
        print(f"[-] {username} отключился")
        broadcast(f"*** {username} вышел из чата ***", username)


def broadcast(message, sender=None):
    for user, conn in clients.items():
        if user != sender:
            try:
                conn.send((message + "\n").encode())
            except:
                pass


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9090))
    server.listen()

    print("Сервер запущен на порту 9090...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
