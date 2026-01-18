import socket
import select

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)
server_socket.setblocking(False)

sockets = [server_socket]

print(f"Listening on http://{HOST}:{PORT}")

while True:
    readable, _, _ = select.select(sockets, [], [])

    for sock in readable:
        # 新しい接続が来た
        if sock is server_socket:
            client_socket, addr = server_socket.accept()
            client_socket.setblocking(False)
            sockets.append(client_socket)
            print("New connection:", addr)

        # 既存クライアントからデータ
        else:
            data = sock.recv(4096)

            if not data:
                print("Disconnected")
                sockets.remove(sock)
                sock.close()
                continue

            print("====== REQUEST ======")
            print(data.decode(errors="replace"))
            print("=====================")

            body = "Hello from event loop!"
            body_bytes = body.encode()

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(body_bytes)}\r\n"
                "\r\n"
            ).encode() + body_bytes

            sock.sendall(response)
