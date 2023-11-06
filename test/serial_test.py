import serial
import sys  # Import the sys module for user input

# 设置串口参数
ser = serial.Serial('COM15', 250000)  # 请将'COM15'替换为你的串口名称
file_count = 1  # 文件计数器，用于创建不同的文件

while True:
    data = ""  # 初始化 data 变量
    data_file = f'serial_data/received_data_{file_count}.txt'  # 创建一个新的文件名
    file_count += 1  # 增加文件计数器以便下一个文件

    # 使用 'w' 模式打开文件，清空文件内容
    with open(data_file, 'w') as file:
        pass  # 不需要执行任何写入操作，只需打开文件以清空内容

    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting).decode('utf-8')  # 以 UTF-8 编码读取串口数据
            with open(data_file, 'a') as file:
                file.write(data)
            print("Received data: " + data)  # 输出到控制台
        if '\n' in data:  # 检查是否接收到换行符
            break  # 如果接收到换行符，停止循环

    # # Check for user input to terminate the script
    # user_input = input("Press 'q' to quit or Enter to continue: ")
    # if user_input.lower() == 'q':
    #     break  # Exit the loop if the user inputs 'Q'

# 关闭串口
ser.close()