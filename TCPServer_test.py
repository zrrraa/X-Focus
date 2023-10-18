import socket

# 设置服务器的主机和端口
host = '192.168.43.226'  # 监听所有网络接口，请将 'localhost' 替换为服务器的IP地址
port = 8888  # 选择一个空闲的端口号

# 创建TCP服务器套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 将套接字绑定到指定的主机和端口
sock.bind((host, port))

# 开始监听连接
sock.listen(1)  # 参数指定允许的最大连接数

print("Server listening on", host, "port", port)

while True:
    # 等待客户端连接
    client_socket, client_address = sock.accept()

    print("Client connected:", client_address)

    while True:
        # 接收客户端数据
        data = client_socket.recv(1024)  # 每次最多接收1024字节的数据

        if not data:  # 如果客户端关闭连接，停止接收数据
            break

        # 在这里处理接收到的数据
        print("Received data from client:", data.decode('utf-8'))

    # 关闭与客户端的连接
    client_socket.close()