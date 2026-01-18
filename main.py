import socket
import select
import os

HOST = "127.0.0.1"
PORT = 8080
WWW_ROOT = "./www"

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
        if sock is server_socket:
            client_socket, addr = server_socket.accept()
            client_socket.setblocking(False)
            sockets.append(client_socket)
            print("New connection:", addr)
            continue

        data = sock.recv(4096)
        if not data:
            sockets.remove(sock)
            sock.close()
            continue

        # ===== STEP5の主役 =====
        request_text = data.decode(errors="replace")
        request_line = request_text.splitlines()[0]
        print("Request line:", request_line)

        try:
            method, path, _ = request_line.split()
        except ValueError:
            sock.close()
            sockets.remove(sock)
            continue

        if path == "/":
            path = "/index.html"

        file_path = WWW_ROOT + path

        if not os.path.isfile(file_path):
            body = "404 Not Found"
            body_bytes = body.encode()
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                f"Content-Length: {len(body_bytes)}\r\n"
                "\r\n"
            ).encode() + body_bytes
        else:
            with open(file_path, "rb") as f:
                body_bytes = f.read()

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(body_bytes)}\r\n"
                "\r\n"
            ).encode() + body_bytes

        sock.sendall(response)
