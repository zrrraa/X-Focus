# CV_Classification

arduino nano 33 ble很神奇，我暂时还不能使用vscode烧录，它的串口会变

运行前将终端位置置于CV_Classification

图像上传，前端网站调用SVM.py对已上传的图像进行分类，通过分类情况生成可视化报告

## 图像分类

参考了https://github.com/chestnut24/SVMImageClassification

添加对test_photo中图片分类的代码

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

## 前端

尝试用一个网站控制分类脚本和监听脚本的运行与中止