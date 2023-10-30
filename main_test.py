import socket
import numpy as np
import struct
from matplotlib import pyplot as plt

# 设置服务器的主机和端口

# lab的host
# host = '192.168.124.7'  # 监听所有网络接口，请将 'localhost' 替换为服务器的IP地址

# 校网ZJUWLAN的host (校网不能用)
# host = '10.162.12.159'

# zrrraa个人热点的host
host = '192.168.43.226'

port = 8090  # 选择一个大于1024的端口号

# 创建TCP服务器套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 将套接字绑定到指定的主机和端口
server_socket.bind((host, port))

# 开始监听连接
server_socket.listen(1)  # 参数指定允许的最大连接数

print("Server listening on", host, "port", port)

# 创建一个列表来存储图像
images = []

file_count = 1  # 文件计数器，用于创建不同的文件

# 初始化浮点数累加变量
float1_sum = 0.0
float2_sum = 0.0
float3_sum = 0.0

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

        if '\n' in received_data:  # 检查是否接收到连续两个换行符，表示一次发送结束
            print("Received data:", data)  # 输出到控制台

            data_file = f'serial_data/received_data_{file_count}.txt'  # 创建一个新的文件名

            # 使用 'w' 模式打开文件，清空文件内容并保存接收到的数据
            with open(data_file, 'w') as file:
                file.write(data)
            
            # 分割数据
            data_parts = data.strip().split(';')

            # 处理浮点数数据
            float_data = [float(x) for x in data_parts[0].split(',')]
            float1_sum += float_data[0]
            float2_sum += float_data[1]
            float3_sum += float_data[2]

            # 更新到文件 "AudioClassfication/audio_record.txt"
            with open("AudioClassfication/audio_record.txt", 'w') as file:
                file.write(f"{float1_sum},{float2_sum},{float3_sum}\n")

            # 处理十六进制数据
            hex_values = data_parts[1].strip().split(',')
            HEXADECIMAL_BYTES = []
            for hex_value in hex_values:
                try:
                    value = int(hex_value, 16)
                    if 0x0 <= value <= 0xffff:
                        HEXADECIMAL_BYTES.append(hex_value.strip())
                    else:
                        HEXADECIMAL_BYTES.append("0x0")
                except ValueError:
                    HEXADECIMAL_BYTES.append("0x0")

            # 补充或舍去多余的数
            HEXADECIMAL_BYTES = HEXADECIMAL_BYTES[:76800]  # 舍去多余的数

            while len(HEXADECIMAL_BYTES) < 76800:  # 用 0x0 补充不足的数
                HEXADECIMAL_BYTES.append("0x0")

            # 将处理后的数据保存到文件
            dealed_data_file = f'serial_data/received_data_dealed_{file_count}.txt'
            with open(dealed_data_file, 'w') as file:
                file.write('\n'.join(HEXADECIMAL_BYTES))

            # 重新格式化字节为图像
            raw_bytes = np.array([int(x, 16) for x in HEXADECIMAL_BYTES], dtype="i2")

            image = np.zeros((len(raw_bytes), 3), dtype=int)

            for j in range(len(raw_bytes)):
                pixel = struct.unpack('>h', raw_bytes[j])[0]
                r = ((pixel >> 11) & 0x1F) << 3
                g = ((pixel >> 5) & 0x3F) << 2
                b = (pixel & 0x1F) << 3
                image[j] = [r, g, b]

            image = np.reshape(image, (240, 320, 3))
            image = np.uint8(image)

            images.append(image)

            output_path = f"SVMImageClassification/test_photo/output_image_{file_count}.png"
            plt.imsave(output_path, image, format='png')

            file_count += 1  # 增加文件计数器以便下一个文件

            data = ""  # 重置数据变量

    # 关闭与客户端的连接
    client_socket.close()