import socket

HOST = "127.0.0.1"
PORT = 8080

# 1. ソケットを作る
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 再起動しやすくする設定
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 3. アドレスとポートを紐づける
server_socket.bind((HOST, PORT))

# 4. 接続待ち状態にする
server_socket.listen(1)

print(f"Listening on http://{HOST}:{PORT}")

# 5. クライアントの接続を待つ
client_socket, client_address = server_socket.accept()
print("Connected from", client_address)

# 6. リクエストを受け取る
request = client_socket.recv(4096)
print("---- request ----")
print(request.decode())
print("-----------------")

# 7. 固定のHTTPレスポンスを返す
response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain\r\n"
    "Content-Length: 13\r\n"
    "\r\n"
    "Hello, world!"
)

client_socket.sendall(response.encode())

# 8. 接続を閉じる
client_socket.close()
server_socket.close()
