# CV_Classification

arduino使用的是Harvard_TinyMLx库中的test_camera.ino例程，注意串口波特率等参数的修改

arduino nano 33 ble很神奇，我暂时还不能使用vscode烧录，它的串口会变

预期完成三步工作：串口有线上传本地，wifi上传本地，wifi上传云服务器

前端网站调用SVM.py对已上传的图像进行分类

## 10.16

串口有线上传图像数据，生成图像文件保存在本地文件夹中

目前给arduino烧录程序后，将终端位置置于CV_Classification，运行test.py，按下按钮后test_photo文件夹中会多一张刚拍的图片。test.py运行后会一直循环，退出需要CTRL+C

## 10.17

branchtest

## 10.18

wifi上传图像数据，生成图像文件保存在本地文件夹中

目前在PC端使用网络调试助手可以收到TCP透传的数据，但是通过py脚本直接获取还未成功，原因未知
