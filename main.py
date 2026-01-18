import socket

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Listening on http://{HOST}:{PORT}")

client_socket, client_address = server_socket.accept()
print("Connected from", client_address)

request = client_socket.recv(4096)
print("====== REQUEST ======")
print(request.decode(errors="replace"))
print("=====================")

# ★ STEP2の主役
body = "Hello, webserv!"
body_bytes = body.encode()

response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain\r\n"
    f"Content-Length: {len(body_bytes)}\r\n"
    "\r\n"
).encode() + body_bytes

client_socket.sendall(response)

client_socket.close()
server_socket.close()
