import socket

socket_ = socket.socket()
socket_.connect(("localhost", 80))
send_data = input("请输入要发送的内容：")
socket_.send(send_data.encode())

# 接收最大1024字节的数据
recv_data = socket_.recv(1024).decode()
print("接收数据：", recv_data)
socket_.close()