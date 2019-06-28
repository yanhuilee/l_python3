# socket accept()

import socket
host = "localhost"
port = 80
web = socket.socket()
web.bind((host, port))
web.listen(5)

print("服务器等待客户端连接。。。")

while True:
    connection, address = web.accept()
    data = connection.recv(1024)
    print("data: ", data)
    connection.sendall(b'HTTP/1/1 200 OK\r\n\r\nHello')
    connection.close()