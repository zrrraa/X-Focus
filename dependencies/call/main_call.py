import socket
import numpy as np
import struct

import os
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import matplotlib as mpl

def run_classification_server(host, port):
    # 创建TCP服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 将套接字绑定到指定的主机和端口
    server_socket.bind((host, port))

    # 开始监听连接
    server_socket.listen(1)  # 参数指定允许的最大连接数

    print("Server listening on", host, "port", port)

    # 创建一个列表来存储图像
    images = []

    # 清空分类情况
    with open('SVMImageClassification/classification_results.txt', 'w') as f:
        pass

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
                with open("AudioClassification/audio_record.txt", 'w') as file:
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

                classify_images(output_path)

                file_count += 1  # 增加文件计数器以便下一个文件

                data = ""  # 重置数据变量

        # 关闭与客户端的连接
        client_socket.close()

def classify_images(image_paths):
    mpl.rcParams['font.sans-serif'] = ['KaiTi']
    mpl.rcParams['font.serif'] = ['KaiTi']

    X = []
    Y = []
    Z = []

    for i in range(0, 4):
        for f in os.listdir("SVMImageClassification/photo3/%s" % i):
            X.append("SVMImageClassification/photo3//" + str(i) + "//" + str(f))
            Y.append(i)

    X = np.array(X)
    Y = np.array(Y)

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        Y,
                                                        test_size=0.3,
                                                        random_state=1)

    print(len(X_train), len(X_test), len(y_train), len(y_test))

    XX_train = []
    for i in X_train:
        image = cv2.imdecode(np.fromfile(i, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.resize(image, (256, 256), interpolation=cv2.INTER_CUBIC)
        hist = cv2.calcHist([img], [0, 1], None, [256, 256],
                            [0.0, 255.0, 0.0, 255.0])
        XX_train.append(((hist / 255).flatten()))

    XX_test = []
    for i in X_test:
        image = cv2.imdecode(np.fromfile(i, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.resize(image, (256, 256), interpolation=cv2.INTER_CUBIC)
        hist = cv2.calcHist([img], [0, 1], None, [256, 256],
                            [0.0, 255.0, 0.0, 255.0])
        XX_test.append(((hist / 255).flatten()))

    clf = SVC().fit(XX_train, y_train)
    clf = SVC(kernel="linear").fit(XX_train, y_train)
    predictions_labels = clf.predict(XX_test)

    print(u'预测结果:')
    print(predictions_labels)
    print(u'算法评价:')
    print(classification_report(y_test, predictions_labels))

    labels = [0, 1, 2, 3]

    y_true = y_test
    y_pred = predictions_labels

    tick_marks = np.array(range(len(labels))) + 0.5

    def plot_confusion_matrix(cm,
                              title='Confusion Matrix',
                              cmap=plt.cm.binary):
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        xlocations = np.array(range(len(labels)))
        plt.xticks(xlocations, labels, rotation=90)
        plt.yticks(xlocations, labels)
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

    cm = confusion_matrix(y_true, y_pred)
    np.set_printoptions(precision=2)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print(cm_normalized)
    plt.figure(1, figsize=(12, 8), dpi=120)

    ind_array = np.arange(len(labels))
    x, y = np.meshgrid(ind_array, ind_array)

    for x_val, y_val in zip(x.flatten(), y.flatten()):
        c = cm_normalized[y_val][x_val]
        if c > 0.01:
            plt.text(x_val,
                     y_val,
                     "%0.2f" % (c, ),
                     color='red',
                     fontsize=7,
                     va='center',
                     ha='center')

    plt.gca().set_xticks(tick_marks, minor=True)
    plt.gca().set_yticks(tick_marks, minor=True)
    plt.gca().xaxis.set_ticks_position('none')
    plt.gca().yaxis.set_ticks_position('none')
    plt.grid(True, which='minor', linestyle='-')
    plt.gcf().subplots_adjust(bottom=0.15)

    plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')

    plt.savefig('SVMImageClassification/matrix.png', format='png')

    results = []

    image = cv2.imread(image_paths)
    img = cv2.resize(image, (256, 256), interpolation=cv2.INTER_CUBIC)
    hist = cv2.calcHist([img], [0, 1], None, [256, 256],
                        [0.0, 2550.0, 0.0, 255.0])
    X_test = ((hist / 255).flatten())
    prediction = clf.predict([X_test])[0]
    results.append((image_paths, prediction))

    # Save results to a text file
    with open('SVMImageClassification/classification_results.txt', 'a') as f:
        for path, prediction in results:
            f.write(f'{path}: {prediction}\n')

    print('分类结果已保存到 classification_results.txt 文件中。')