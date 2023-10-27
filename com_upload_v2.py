import serial
import sys  # 导入 sys 模块以获取用户输入

import numpy as np
import struct
from matplotlib import pyplot as plt

# 设置串口参数
ser = serial.Serial('COM15', 115200)  # 请将'COM15'替换为你的串口名称
file_count = 1  # 文件计数器，用于创建不同的文件

# 创建一个列表来存储图像
images = []

while True:
    data = ""  # 初始化 data 变量
    data_file = f'serial_data/received_data_{file_count}.txt'  # 创建一个新的文件名

    # 使用 'w' 模式打开文件，清空文件内容
    with open(data_file, 'w') as file:
        pass  # 只需打开文件以清空内容，不需要执行任何写入操作

    HEXADECIMAL_BYTES = []  # 在循环之外初始化列表

    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting).decode('utf-8')  # 以 UTF-8 编码读取串口数据
            with open(data_file, 'a') as file:
                file.write(data)
            print("Received data: " + data)  # 输出到控制台
        if '\n' in data:  # 检查是否接收到换行符
            break  # 如果接收到换行符，停止循环

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

    image = np.reshape(image, (240, 320, 3))
    image = np.uint8(image)

    images.append(image)

    output_path = f"SVMImageClassification/test_photo/output_image_{file_count}.png"
    plt.imsave(output_path, image, format='png')

    file_count += 1  # 增加文件计数器以便下一个文件