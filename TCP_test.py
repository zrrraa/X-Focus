import socket

# 设置TCP服务器的主机和端口
host = '192.168.124.7'  # 请将 'localhost' 替换为服务器主机名或IP地址
port = 8040  # 请将 1234 替换为服务器端口号

# 建立TCP连接
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

print("connect success!")

while True:
    data = sock.recv(1024)  # 接收数据，每次最多接收1024字节

    if not data:  # 如果接收到空数据，表示连接已关闭
        break

    # 在这里处理接收到的数据
    print("Received data:", data.decode('utf-8'))

# 关闭TCP连接
sock.close()