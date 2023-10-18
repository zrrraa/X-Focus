import socket
import numpy as np
import struct
from matplotlib import pyplot as plt

# 设置服务器的主机和端口
host = '192.168.43.226'  # 监听所有网络接口，请将 'localhost' 替换为服务器的IP地址
port = 8040  # 选择一个大于1024的端口号

# 创建TCP服务器套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 将套接字绑定到指定的主机和端口
server_socket.bind((host, port))

# 开始监听连接
server_socket.listen(1)  # 参数指定允许的最大连接数

print("Server listening on", host, "port", port)

# 创建一个列表来存储图像
images = []

file_count =1 # 文件计数器，用于创建不同的文件
while True:
    # 等待客户端连接
    client_socket, client_address = server_socket.accept()

    print("Client connected:", client_address)

    data = ""  # 初始化 data 变量

    while True:
        received_data = client_socket.recv(1024).decode('utf-8')  # 以 UTF-8 解码接收客户端数据

        if not received_data:  # 如果客户端关闭连接，停止接收数据
            break

        data += received_data

        if '\n' in received_data:  # 检查是否接收到换行符
            data_file = f'serial_data/received_data_{file_count}.txt'  # 创建一个新的文件名

            # 使用 'w' 模式打开文件，清空文件内容
            with open(data_file, 'w') as file:
                file.write(data)

            print("Received data:", data)  # 输出到控制台

            HEXADECIMAL_BYTES = []  # 在循环之外初始化列表

            # 打开当前 txt 文件并读取每一行，然后将每一行分割成十六进制值
            with open(data_file, "r") as file:
                for line in file:
                    hex_values = line.strip().split(',')
                    for hex_value in hex_values:
                        HEXADECIMAL_BYTES.append(hex_value.strip())

            # 重新格式化字节为图像
            raw_bytes = np.array([int(x, 16) for x in HEXADECIMAL_BYTES if x], dtype="i2")
            image = np.zeros((len(raw_bytes), 3), dtype=int)

            for j in range(len(raw_bytes)):
                pixel = struct.unpack('>h', raw_bytes[j])[0]
                r = ((pixel >> 11) & 0x1F) << 3
                g = ((pixel >> 5) & 0x3F) << 2
                b = (pixel & 0x1F) << 3
                image[j] = [r, g, b]

            image = np.reshape(image, (144, 176, 3))
            image = np.uint8(image)

            images.append(image)

            output_path = f"SVMImageClassification/test_photo/output_image_{file_count}.png"
            plt.imsave(output_path, image, format='png')

            file_count += 1  # 增加文件计数器以便下一个文件

            data = ""  # 重置数据变量

    # 关闭与客户端的连接
    client_socket.close()