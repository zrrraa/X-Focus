# CV_Classification

运行mymain.py

图像和噪声上传并进行分类，前端通过分类情况生成可视化报告

## 转接板

[调试文档](https://xn4zlkzg4p.feishu.cn/wiki/DSxzwSo8iiLLURkXnTMca9K1nwh?from=from_copylink)

官方转接板原理图 [官方](https://content.arduino.cc/assets/MachineLearningCarrierV1.0.pdf)

自制转接板 [自制](https://pro.lceda.cn/editor#id=f7357ab4b7e142e686c2cabcdf9fad5d)

## 图像分类

参考了 [SVMImageClassification](https://github.com/chestnut24/SVMImageClassification)

## 噪声分类

[噪声分类](https://xn4zlkzg4p.feishu.cn/wiki/Ftn9wbrffiWQCpkAhVVcfoKCn7d?from=from_copylink)

参考Edge Impulse网站的噪声分类教程，训练后导出库，arduino直接计算出分类结果并上传

## 上传

预期路径：串口有线上传本地——>wifi无线上传本地——>wifi上传云端

上传本地中，上传的图片均储存在SVMImageClassification/test_photo中

### 串口有线上传本地

arduino的程序为test_camera.ino

给arduino烧录程序后，运行com_upload.py，按下按钮后会进行一次拍照和上传图片。com_upload.py运行后会一直循环

### wifi无线上传本地

arduino的程序为wifi_upload.ino

esp-01做客户端，PC端做服务器，通过TCP协议传输数据

给arduino烧录程序后，运行wifi_upload.py，按下按钮后会进行一次拍照和上传图片。wifi_upload.py运行后会一直循环

arduino与esp-01的串口通信采用软串口的形式

## 前端

[前端](https://xn4zlkzg4p.feishu.cn/wiki/MMwnwaufji8mv3kawXqcMhXpn4b?from=from_copylink)

pyQT开发，将txt数据全读到数据库中，再显示分类

## 不重要的事

arduino nano 33 ble很神奇，我暂时还不能使用vscode烧录，它的串口会变

ov7675的官方转接板原理图D10和D1接线反了，layout是对的

在tinymlsheld头文件中更改摄像头的IO口连接，在电路上用杜邦线更改，出来的图像很奇怪，不确定是否也是受电磁干扰影响

arduino nano 33 ble无法使用SoftwareSerial，不过可以使用UART库

```
UART softSerial2(digitalPinToPinName(2), digitalPinToPinName(0), NC, NC);
```

这句代码开启2脚和0脚做软串口，为什么连1脚和0脚也能进行串口收发？想不明白
