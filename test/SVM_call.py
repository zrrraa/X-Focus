import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import matplotlib as mpl


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