import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice

#导入串口模块
from dependencies.window_ui.main_ui import Ui_Form
import serial.tools.list_ports

#导入画图模块
import pyqtgraph as pg

#数字处理，取对数
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#以下为主线程函数
from dependencies.window_ui.login_window import Ui_login
import time
from dependencies.window_ui.signup import Ui_signup
import sqlite3
import numpy as np
import random
import datetime
import socket
import struct
from matplotlib import pyplot as plt

import os
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC
import matplotlib as mpl

zhanghao_now = ''
status_list = []

#本工程运用三个数据库，分别存储用户账号信息(user_index),用户登录信息（user_login),
# 用户学习信息（user_info）
#sql3 = sqlite3.connect("user_index.db")
#sql3.execute("create table users (id integer primary key,zhanghao varchar(10) UNIQUE,mima text NULL)")#建立表格

#sql3 = sqlite3.connect("user_login.db")
#sql3.execute("create table users_login (id integer primary key, zhanghao varchar(10) ,time text NULL)")#建立表格

#sql3 = sqlite3.connect("user_status_classfication.db")
#sql3.execute("create table users_status_classfication (id integer primary key AUTOINCREMENT, zhanghao varchar(10) ,totaltime integer,today varchar(10),computer integer, phone integer,read integer,left integer)")#建立表格

#sql3 = sqlite3.connect("user_audio_classfication.db")
#sql3.execute("create table users_audio_classfication (id integer primary key AUTOINCREMENT, zhanghao varchar(10) ,totaltime integer,today varchar(10),decorating real, noise real, whistling real)")#建立表格

#cur=sql3.cursor()
'''for t in[(1,'张三',0.33,0.66,0.999),(0,'李四',0.66,0.77,0.88)]:
 
  cur.execute("insert into users_audio_classfication (zhanghao,total,train,cough,other) values (?,?,?,?,?)", t)
  last_id = cur.lastrowid
  print(str(last_id))
  sql3.commit()'''
# 获取当前日期
#current_date = datetime.datetime.now().date()
#print( current_date)


class MysignupForm(QMainWindow, Ui_signup):

    def __init__(self):
        #这里需要重载一下Login_window，同时也包含了QtWidgets.QMainWindow的预加载项。

        super(MysignupForm, self).__init__()
        self.signup_ui = Ui_signup()
        self.signup_ui.setupUi(self)
        self.signup_ui.sql3 = sqlite3.connect(
            'dependencies/database/user_index.db')  #建立数据库/连接数据库
        self.signup_ui.sign_up_button.clicked.connect(
            self.signup_db)  #与数据库更新查询函数进行连接
        self.signup_ui.back_button.clicked.connect(
            self.back_up)  #与数据库更新查询函数进行连接

        self.setGeometry(250, 50, 1200, 800)
        self.signup_ui.palette = QPalette()
        #self.setWindowFlag(Qt.FramelessWindowHint)  #取消边框
        #self.setWindowFlags(Qt.WindowMinMaxButtonsHint)
        #self.signup_ui.palette.setBrush(QPalette.backgroundRole(), QBrush(QPixmap("images/login_1.png")))
        self.signup_ui.palette.setBrush(
            MysignupForm.backgroundRole(self),
            QBrush(
                QPixmap("dependencies/images/signup.jpg").scaled(
                    MysignupForm.size(self), QtCore.Qt.IgnoreAspectRatio,
                    QtCore.Qt.SmoothTransformation)))
        self.signup_ui.op1 = QtWidgets.QGraphicsOpacityEffect()
        self.signup_ui.op2 = QtWidgets.QGraphicsOpacityEffect()
        self.signup_ui.op3 = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        self.signup_ui.op1.setOpacity(0.8)
        self.signup_ui.op2.setOpacity(0.9)
        self.signup_ui.op3.setOpacity(0.9)

        self.signup_ui.label_4.setGraphicsEffect(self.signup_ui.op1)
        self.signup_ui.back_button.setGraphicsEffect(self.signup_ui.op2)
        self.signup_ui.sign_up_button.setGraphicsEffect(self.signup_ui.op3)
        self.signup_ui.label_4.setStyleSheet(
            '''QLabel{background:#FFFFFF;border-radius:20px;}QLabel{;font-size:30px;color:rgb(200,200,200);}'''
        )

        self.signup_ui.back_button.setStyleSheet(
            '''QPushButton{background:#111111;border-radius:5px;}QPushButton:hover{background:#333333;}QPushButton{;font-size:30px;color:rgb(207,181,59);font-family : '微软雅黑';}'''
        )
        self.signup_ui.sign_up_button.setStyleSheet(
            '''QPushButton{background:#111111;border-radius:5px;}QPushButton:hover{background:#333333;}QPushButton{;font-size:30px;color:rgb(207,181,59);font-family : '微软雅黑';}'''
        )
        #self.signup_ui.backup.setStyleSheet('''QPushButton{background:#222222;border-radius:5px;}QPushButton:hover{background:grey;}''')
        self.signup_ui.thelogo.setPixmap(
            QPixmap('dependencies/images/logo.png').scaled(
                self.signup_ui.thelogo.size()))
        self.signup_ui.label_5.setStyleSheet(
            '''QLabel{font-size:30px;color:rgb(33,33,33);font-family : '微软雅黑';}'''
        )
        self.signup_ui.label.setStyleSheet(
            '''QLabel{font-size:20px;color:rgb(33,33,33);font-family : '微软雅黑';}'''
        )
        self.signup_ui.label_2.setStyleSheet(
            '''QLabel{font-size:20px;color:rgb(33,33,33);font-family : '微软雅黑';}'''
        )
        self.signup_ui.label_3.setStyleSheet(
            '''QLabel{font-size:20px;color:rgb(33,33,33);font-family : '微软雅黑';}'''
        )

        self.signup_ui.zhanghao.setStyleSheet(
            '''QLabel{font-size:15px;color:rgb(33,33,33);font-family : '微软雅黑';}'''
        )
        self.signup_ui.mima.setStyleSheet(
            '''QLabel{font-size:15px;color:rgb(33,33,33);font-family : '微软雅黑';}'''
        )
        self.signup_ui.querenmima.setStyleSheet(
            '''QLabel{font-size:15px;color:rgb(33,33,33);font-family : '微软雅黑';}'''
        )

        self.setPalette(self.signup_ui.palette)

    def back_up(self):
        mysignup.close()
        mylogin.show()

    def signup_db(self):
        self.signup_ui.cursor = self.signup_ui.sql3.cursor()
        self.signup_ui.results = self.signup_ui.cursor.execute(
            "SELECT * FROM users")
        self.signup_ui.users = self.signup_ui.results.fetchall()  # 结果转成元组
        self.signup_ui.flag = 0  #标志位

        for user in self.signup_ui.users:  #获取表格内数据
            if (user[1] == self.signup_ui.zhanghao.text()):
                self.signup_ui.flag = 1

        if (self.signup_ui.zhanghao.text()
                == '') or ((self.signup_ui.mima.text() == '')):
            result2 = QMessageBox.critical(
                self, "错误", "<font color=\"#000000\">请输入完整</font>",
                QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)  #有空着的

        elif (self.signup_ui.flag == 1):
            result2 = QMessageBox.critical(
                self, "错误", "<font color=\"#000000\">您输入了同样的账号</font>",
                QMessageBox.Ok | QMessageBox.Cancel,
                QMessageBox.Cancel)  #重复输入了账号

        elif (self.signup_ui.flag == 0):
            if self.signup_ui.mima.text() == self.signup_ui.querenmima.text():
                id = len(self.signup_ui.users)

                user_info = [
                    id,
                    self.signup_ui.zhanghao.text(),
                    self.signup_ui.mima.text()
                ]  #进行数据的输入
                self.signup_ui.sql3.execute("insert into users values (?,?,?)",
                                            user_info)
                self.signup_ui.sql3.commit()  #上传至数据库

                result2 = QMessageBox.information(
                    self, "信息", "<font color=\"#000000\">注册成功</font>",
                    QMessageBox.Ok | QMessageBox.Cancel,
                    QMessageBox.Cancel)  #成功
                mysignup.close()
                mylogin.show()

            else:
                result2 = QMessageBox.critical(
                    self, "错误", "<font color=\"#000000\">密码不一致</font>",
                    QMessageBox.Ok | QMessageBox.Cancel,
                    QMessageBox.Cancel)  #密码不一致


class MyloginForm(QMainWindow, Ui_login):

    def __init__(self):
        #这里需要重载一下Login_window，同时也包含了QtWidgets.QMainWindow的预加载项。
        super(MyloginForm, self).__init__()
        self.login_ui = Ui_login()
        self.login_ui.setupUi(self)
        self.setWindowTitle("登录界面")

        self.login_ui.sql3 = sqlite3.connect(
            "dependencies/database/user_index.db")  #建立数据库/连接数据库
        self.setGeometry(250, 50, 1200, 800)
        self.login_ui.palette = QPalette()
        #self.setWindowFlag(Qt.FramelessWindowHint)  #取消边框
        #self.setWindowFlags(Qt.WindowMinMaxButtonsHint)
        #self.signup_ui.palette.setBrush(QPalette.backgroundRole(), QBrush(QPixmap("images/login_1.png")))
        self.login_ui.palette.setBrush(
            MyloginForm.backgroundRole(self),
            QBrush(
                QPixmap("dependencies/images/login_1.png").scaled(
                    MyloginForm.size(self), QtCore.Qt.IgnoreAspectRatio,
                    QtCore.Qt.SmoothTransformation)))
        self.login_ui.op1 = QtWidgets.QGraphicsOpacityEffect()
        self.login_ui.op2 = QtWidgets.QGraphicsOpacityEffect()
        self.login_ui.op3 = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        self.login_ui.op1.setOpacity(0.7)
        self.login_ui.op2.setOpacity(0.7)
        self.login_ui.op3.setOpacity(0.7)

        self.login_ui.login_button.setGraphicsEffect(self.login_ui.op1)
        self.login_ui.signup_button.setGraphicsEffect(self.login_ui.op2)
        self.login_ui.backup.setGraphicsEffect(self.login_ui.op3)
        self.login_ui.login_button.setStyleSheet(
            '''QPushButton{background:#222222;border-radius:5px;}QPushButton:hover{background:grey;}QPushButton{;font-size:30px;color:rgb(200,200,200);}'''
        )
        self.login_ui.signup_button.setStyleSheet(
            '''QPushButton{background:#222222;border-radius:5px;}QPushButton:hover{background:grey;}QPushButton{;font-size:30px;color:rgb(200,200,200);}'''
        )
        self.login_ui.backup.setStyleSheet(
            '''QPushButton{background:#222222;border-radius:5px;}QPushButton:hover{background:grey;}'''
        )
        #self.zhanghao.setStyleSheet("background-color: rgba(255, 132, 139, 0);color : rgb(13,118,114);font-size : 34px;font-family : '微软雅黑';")
        self.login_ui.label.setStyleSheet(
            '''QLabel{color:rgb(230,230,230);}''')
        self.login_ui.label_2.setStyleSheet(
            '''QLabel{color:rgb(230,230,230);}''')
        self.login_ui.label_3.setPixmap(
            QPixmap('dependencies/images/logo.png').scaled(
                self.login_ui.label_3.size()))

        self.setPalette(self.login_ui.palette)

        self.login_ui.login_button.clicked.connect(self.success_sign_in)
        self.login_ui.signup_button.clicked.connect(self.signup)
        self.login_ui.backup.clicked.connect(self.backup)

    def backup(self):
        mylogin.close()

    def signup(self):
        mylogin.close()
        mysignup.show()  #界面跳转

    def success_sign_in(self):

        self.login_ui.cursor = self.login_ui.sql3.cursor()
        self.login_ui.results = self.login_ui.cursor.execute(
            "SELECT * FROM users")
        self.login_ui.users = self.login_ui.results.fetchall()  # 结果转成元组
        self.login_ui.flag = 0  #标志位

        for user in self.login_ui.users:  #获取表格内数据
            if (user[1] == self.login_ui.zhanghao.text()) and (
                    user[2] == self.login_ui.mima.text()):
                self.login_ui.flag = 1  #标志位
            #print("输入正确")
            #1打开新窗口
        if (self.login_ui.flag == 1):
            self.login_ui.sql_login = sqlite3.connect(
                "dependencies/database/user_login.db")  #建立数据库/连接数据库
            self.login_ui.cursor_login = self.login_ui.sql_login.cursor()
            self.login_ui.results_login = self.login_ui.cursor_login.execute(
                "SELECT COUNT(*) FROM users_login")

            #print(len(self.login_ui.users_login))
            user_info = [
                int(self.login_ui.cursor_login.fetchone()[0]),
                self.login_ui.zhanghao.text(),
                str((QDateTime.currentDateTime()).toString())
            ]  #数据库记载登陆记录
            self.login_ui.sql_login.execute(
                "insert into users_login values (?,?,?)", user_info)
            self.login_ui.sql_login.commit()  #上传至数据库
            global zhanghao_now
            zhanghao_now = self.login_ui.zhanghao.text()
            self.login_ui.zhanghao.setText('')
            self.login_ui.mima.setText('')
            #print(zhanghao_now)
            '''
            self.login_ui.results_login = self.login_ui.cursor_login.execute("SELECT * FROM users_login WHERE zhanghao = 'test1'")
            for row in self.login_ui.results_login:
                print(row)
            print("hello world")'''
            result2 = QMessageBox.information(
                self, "信息", "<font color=\"#000000\">登录成功</font>",
                QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)  #成功

            self.login_ui.sql_login.close()  #关闭数据库连接

            mylogin.close()
            mymain.show()
            mymain.data_update()  #可以直接调用函数进行操作
            #2关闭本窗口
        else:
            result2 = QMessageBox.critical(
                self, "错误", "<font color=\"#000000\">账号或者密码错误</font>",
                QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)  #成功


class MyMainForm(QMainWindow, Ui_Form):  #创建MyMainForm类，继承两个类（在MyUi中定义）的属性与方法

    def __init__(self, parent=None):  #为实例加上需要的属性，初始化参数parent，下列均需要此参数
        #没有parent的类应为最上层的窗体，保证child再主窗体在回收时也被回收
        # super()用来调用父类(基类)的方法,super().__init__() 就是调用父类的init方法，父类为MyMainForm
        super(MyMainForm, self).__init__(parent)
        self.ui = Ui_Form()  #创建一个名为ui的实例对象，该对象是UI_Dialog的一个实例
        self.ui.palette = QPalette()
        #qApp.setStyleSheet()
        self.ui.setupUi(self)  #初始化主窗口，调用ui对象的初始化方法
        self.setWindowTitle("X-Peer")
        
        #self.setWindowFlag(Qt.FramelessWindowHint)  #取消边框
        self.ui.op1 = QtWidgets.QGraphicsOpacityEffect()
        self.ui.op2 = QtWidgets.QGraphicsOpacityEffect()
        self.ui.op3 = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        self.ui.op1.setOpacity(0.9)
        self.ui.op2.setOpacity(0.9)
        self.ui.op3.setOpacity(0.9)

        self.ui.log_out.setGraphicsEffect(self.ui.op1)
        self.ui.start_button.setGraphicsEffect(self.ui.op2)
        self.ui.stop_button.setGraphicsEffect(self.ui.op3)
        self.ui.start_button.setStyleSheet(
            '''QPushButton{background:#222222;border-radius:15px;}QPushButton:hover{background:grey;}QPushButton{;font-size:30px;color:rgb(200,200,200);}'''
        )
        self.ui.stop_button.setStyleSheet(
            '''QPushButton{background:#222222;border-radius:15px;}QPushButton:hover{background:grey;}QPushButton{;font-size:30px;color:rgb(200,200,200);}'''
        )
        self.ui.log_out.setStyleSheet(
            '''QPushButton{background:#222222;border-radius:15px;}QPushButton:hover{background:grey;}QPushButton{;font-size:30px;color:rgb(200,200,200);}'''
        )

        self.data_rec = Son_thread_data_rec(self)  #创建一个子线程，用于接受相关数据，防止阻塞
        self.data_rec.son_signal1.connect(
            self.create_piechart)  # 将子线程的信号连接到主线程的画饼函数
        self.data_rec.son_signal1.connect(
            self.create_piechart_status)  # 将子线程的信号连接到主线程的status画饼函数
        self.timer = QTimer(self)  #实例化定时器，用于计时
        self.timer.timeout.connect(self.time_update)  #进行跳转

        #self.ui.start_button.clicked.connect(self.create_piechart)
        self.ui.start_button.clicked.connect(self.start_thread)  #点击开始计时按钮后开启线程
        self.ui.stop_button.clicked.connect(self.stop_thread)  #点击关闭按钮后结束线程
        self.ui.pushButton_4.clicked.connect(self.close_page)
        self.ui.log_out.clicked.connect(self.back_log)

        self.ui.label_15.setPixmap(
            QPixmap('dependencies/images/icons' + '/time.png').scaled(
                self.ui.label_15.size(), QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation))  #后面两个命令用于抗锯齿
        self.ui.label_17.setPixmap(
            QPixmap('dependencies/images/icons' + '/noise.png').scaled(
                self.ui.label_17.size(), QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation))  #后面两个命令用于抗锯齿
        self.ui.label_18.setPixmap(
            QPixmap('dependencies/images/icons' + '/hardworking.png').scaled(
                self.ui.label_18.size(), QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation))  #后面两个命令用于抗锯齿
        self.ui.label_19.setPixmap(
            QPixmap('dependencies/images/icons' + '/compare.png').scaled(
                self.ui.label_19.size(), QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation))  #后面两个命令用于抗锯齿
        self.setGeometry(250, 50, 1200, 800)
        '''self.create_piechart()
        self.show()'''
        #self.data_update()
        self.time_total = 0

    def back_log(self):
        mymain.close()
        mylogin.show()

    def output_result(self):
        #先进行时间与状态数据的计算
        self.ui.sql_status = sqlite3.connect(
            "dependencies/database/user_status_classfication.db")  #连接数据库进行数据的存储,存储相应的状态
        self.ui.cur_status = self.ui.sql_status.cursor()  #进行游标的设置
        self.ui.status_results = self.ui.cur_status.execute(
            "SELECT * FROM users_status_classfication")
        self.ui.status_xiangxis = self.ui.status_results.fetchall()  # 结果转成元组
        last_id = self.ui.cur_status.lastrowid
        status_list_today = [0, 0, 0, 0, 0]
        status_list_lasttime = [0, 0, 0, 0, 0]
        status_list_thistime = [0, 0, 0, 0, 0]
        for xiangxi in self.ui.status_xiangxis:  #获取表格内数据
            #print(self.ui.status_xiangxis[last_id-1])#获取最新一行
            if (xiangxi[1] == zhanghao_now):
                status_list_thistime[0] = xiangxi[2]
                status_list_thistime[1] = xiangxi[4]
                status_list_thistime[2] = xiangxi[5]
                status_list_thistime[3] = xiangxi[6]
                status_list_thistime[4] = xiangxi[7]

                if (xiangxi[3] == self.ui.status_xiangxis[last_id - 1][3]):

                    status_list_today[0] += xiangxi[2]
                    status_list_today[1] += xiangxi[4]
                    status_list_today[2] += xiangxi[5]
                    status_list_today[3] += xiangxi[6]
                    status_list_today[4] += xiangxi[7]  #进行数据的统计，用于计算时长与百分比
        length = (len(self.ui.status_xiangxis))
        for i in range(length - 2, -1, -1):
            print(self.ui.status_xiangxis[i])
            print(self.ui.status_xiangxis[length - 1])
            if (self.ui.status_xiangxis[i][3] == self.ui.status_xiangxis[
                    length - 1][3]):
                if (self.ui.status_xiangxis[i][1] == self.ui.status_xiangxis[
                        length - 1][1]):

                    status_list_lasttime[0] = self.ui.status_xiangxis[i][2]
                    status_list_lasttime[1] = self.ui.status_xiangxis[i][4]
                    status_list_lasttime[2] = self.ui.status_xiangxis[i][5]
                    status_list_lasttime[3] = self.ui.status_xiangxis[i][6]
                    status_list_lasttime[4] = self.ui.status_xiangxis[i][7]
                    print(print(self.ui.status_xiangxis[i]))
                    break
        print(status_list_lasttime)
        print(status_list_thistime)

        #print(status_list_today)
        #print(str(last_id))
        status_list_today_total = status_list_today[1] + status_list_today[
            2] + status_list_today[3] + status_list_today[4]
        status_list_lasttime_total = status_list_lasttime[
            1] + status_list_lasttime[2] + status_list_lasttime[
                3] + status_list_lasttime[4]
        status_list_thistime_total = status_list_thistime[
            1] + status_list_thistime[2] + status_list_thistime[
                3] + status_list_thistime[4]
        #status_list_thistime=self.ui.status_xiangxis[last_id-1]
        self.ui.label_21.setText('报告已生成')
        self.ui.time_data.setText('您今天已经学习了' + str(status_list_today[0]) +
                                  '分钟,上次学习时间为' + str(status_list_lasttime[0]) +
                                  '分钟，此次学习时间为' + str(status_list_thistime[0]) +
                                  '分钟')

        self.ui.study_screen_data_.setText(
            '本次学习中，您有' + str(
                round((status_list_thistime[1] / status_list_thistime_total) *
                      100, 1)) + '%时间在电脑上,' + '有' +
            str(
                round((status_list_thistime[2] / status_list_thistime_total) *
                      100, 1)) + '%时间在手机上,' + '有' +
            str(
                round((status_list_thistime[3] / status_list_thistime_total) *
                      100, 1)) + '%时间在书本上。' + '上次学习时间占比' +
            str(
                round(((status_list_lasttime[1] + status_list_lasttime[3]) /
                       status_list_lasttime_total) * 100, 1)) + '%。' +
            '今天总学习时间占比' + str(
                round(((status_list_today[1] + status_list_today[3]) /
                       status_list_today_total) * 100, 1)) + '%。')
        self.ui.cur_status.close()
        self.ui.sql_status.close()

        #接下来进行噪声的测试
        self.ui.sql_audio = sqlite3.connect(
            "dependencies/database/user_audio_classfication.db")  #连接数据库进行数据的存储,存储相应的状态
        self.ui.cur_audio = self.ui.sql_audio.cursor()  #进行游标的设置
        self.ui.audio_results = self.ui.cur_audio.execute(
            "SELECT * FROM users_audio_classfication")
        self.ui.audio_xiangxis = self.ui.audio_results.fetchall()  # 结果转成元组
        last_id = self.ui.cur_audio.lastrowid
        audio_list_today = [0.0, 0.0, 0.0, 0.0, 0.0]
        audio_list_lasttime = [0.0, 0.0, 0.0, 0.0, 0.0]
        audio_list_thistime = [0.0, 0.0, 0.0, 0.0, 0.0]

        for xiangxi in self.ui.audio_xiangxis:  #获取表格内数据
            #print(self.ui.status_xiangxis[last_id-1])#获取最新一行
            if (xiangxi[1] == zhanghao_now):
                audio_list_thistime[1] = xiangxi[4]
                audio_list_thistime[2] = xiangxi[5]
                audio_list_thistime[3] = xiangxi[6]

                if (xiangxi[3] == self.ui.audio_xiangxis[last_id - 1][3]):

                    audio_list_today[1] += xiangxi[4]
                    audio_list_today[2] += xiangxi[5]
                    audio_list_today[3] += xiangxi[6]

        length = (len(self.ui.audio_xiangxis))
        for i in range(length - 2, -1, -1):
            #print(self.ui.status_xiangxis[i])
            if (self.ui.audio_xiangxis[i][3] == self.ui.audio_xiangxis[length -
                                                                       1][3]):
                if (self.ui.audio_xiangxis[i][1] == self.ui.audio_xiangxis[
                        length - 1][1]):

                    audio_list_lasttime[1] = self.ui.audio_xiangxis[i][4]
                    audio_list_lasttime[2] = self.ui.audio_xiangxis[i][5]
                    audio_list_lasttime[3] = self.ui.audio_xiangxis[i][6]

                    break

        noise_label = ['装修类低频噪声', '白噪音', '交通噪音']

        audio_list_today_total = audio_list_today[1] + audio_list_today[
            2] + audio_list_today[3]
        audio_list_lasttime_total = audio_list_lasttime[
            1] + audio_list_lasttime[2] + audio_list_lasttime[3]
        audio_list_thistime_total = audio_list_thistime[
            1] + audio_list_thistime[2] + audio_list_thistime[3]

        today_max = audio_list_today.index(max(audio_list_today))
        lasttime_max = audio_list_lasttime.index(max(audio_list_lasttime))
        thistime_max = audio_list_thistime.index(max(audio_list_thistime))

        self.ui.noise_data.setText(
            '此次学习周边环境噪声,占比最大的是' + noise_label[thistime_max - 1] + ',为' + str(
                round((audio_list_thistime[thistime_max] /
                       audio_list_thistime_total) * 100, 1)) + '%。' +
            '。上次噪声占比最大的是' + noise_label[lasttime_max - 1] + ',为' + str(
                round((audio_list_lasttime[lasttime_max] /
                       audio_list_lasttime_total) * 100, 1)) + '%。' +
            '。今天噪声占比最大的是' + noise_label[today_max - 1] + ',为' + str(
                round((audio_list_today[today_max] / audio_list_today_total) *
                      100, 1)) + '%。')

        if (round(((status_list_today[2] + status_list_today[4]) /
                   status_list_today_total) * 100, 1) > 50):
            if (round(((status_list_today[2]) / status_list_today_total) * 100,
                      1) > 25):
                self.ui.label_22.setText('请专心学习,减少手机使用时间')
            elif (round(
                ((status_list_today[4]) / status_list_today_total) * 100, 1) >
                  25):
                self.ui.label_22.setText('请专心学习,坐住冷板凳')

        elif (round(((status_list_today[1] + status_list_today[2]) /
                     status_list_today_total) * 100, 1) > 50):
            self.ui.label_22.setText('请注意屏幕时长,保护眼睛健康')

        else:
            self.ui.label_22.setText('加油,你做得很棒！')

    def close_page(self):
        mymain.close()
        mylogin.show()

    def data_update(self):  #在另一个窗口中调用
        global zhanghao_now
        #print(zhanghao_now+'= xyz')
        self.ui.user_name_label.setText('   ' + zhanghao_now + ' ')
        self.ui.palette = QPalette()

        self.ui.touxiang.setPixmap(
            QPixmap('dependencies/images/' +
                    zhanghao_now + '_touxiang.png').scaled(
                        self.ui.touxiang.size(), QtCore.Qt.IgnoreAspectRatio,
                        QtCore.Qt.SmoothTransformation))  #后面两个命令用于抗锯齿

    def stop_thread(self):
        self.data_rec.terminate()  #结束子线程
        self.timer.stop()  #关闭计时器

        list = self.read_txt_audio()  #读取此时文件内部的数值

        self.ui.sql_audio = sqlite3.connect(
            "dependencies/database/user_audio_classfication.db")  #连接数据库进行数据的存储
        self.ui.cur_audio = self.ui.sql_audio.cursor()  #进行游标的设置
        current_date = datetime.datetime.now().date()
        t = (zhanghao_now, self.time_total // 60, current_date, float(list[0]),
             float(list[1]), float(list[1]))
        self.ui.cur_audio.execute(
            "insert into users_audio_classfication (zhanghao,totaltime,today,decorating,noise,whistling) values (?,?,?,?,?,?)",
            t)
        last_id = self.ui.cur_audio.lastrowid
        #print(str(last_id))
        self.ui.sql_audio.commit()  #存储
        self.ui.cur_audio.close()
        self.ui.sql_audio.close()

        global status_list
        list = status_list
        computer = self.count_elements(list, 0)
        phone = self.count_elements(list, 1)
        book = self.count_elements(list, 2)
        left = self.count_elements(list, 3)

        self.ui.sql_status = sqlite3.connect(
            "dependencies/database/user_status_classfication.db")  #连接数据库进行数据的存储,存储相应的状态
        self.ui.cur_status = self.ui.sql_status.cursor()  #进行游标的设置
        current_date = datetime.datetime.now().date()

        t = (zhanghao_now, self.time_total // 60, current_date, computer,
             phone, book, left)
        if (computer + phone + book + left > 0):
            self.ui.cur_status.execute(
                "insert into users_status_classfication (zhanghao,totaltime,today,computer, phone,read,left) values (?,?,?,?,?,?,?)",
                t)
            #不存入全0
            last_id = self.ui.cur_status.lastrowid
            #print(str(last_id))
            self.ui.sql_status.commit()  #存储
            #print(list)
            #print(book)
            #print(computer)
            self.ui.cur_status.close()
            self.ui.sql_status.close()
            self.time_total = 0  #时间归零
            status_list = []
            self.output_result()
        else:
            result2 = QMessageBox.critical(
                self, "错误", "<font color=\"#000000\">时间太短！</font>",
                QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)  #成功

    def time_update(self):
        self.time_total += 1
        second = self.time_total % 60
        minutes = (self.time_total // 60) % 60
        hour = ((self.time_total // 60) // 60) % 60
        #print(str(hour)+':'+str(minutes)+':'+str(second))
        second_str = str(second).zfill(2)
        minutes_str = str(minutes).zfill(2)
        hour_str = str(hour).zfill(2)
        self.ui.time_label.setText(hour_str + ':' + minutes_str + ':' +
                                   second_str)

    def start_timer(self):
        self.timer.start(1000)

    def start_thread(self):
        result2 = QMessageBox.information(
            self, "提示", "<font color=\"#000000\">开始学习</font>",
            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)  #成功

        self.data_rec.start()  #开启子线程
        self.start_timer()
        self.ui.label_21.setText('报告尚未生成')
        self.ui.time_data.setText('the data of time')
        self.ui.noise_data.setText('the data of noise')
        self.ui.study_screen_data_.setText('the specific use of time')
        self.ui.label_22.setText('the suggestions')

    def read_txt_audio(self):
        with open('AudioClassification/audio_record.txt', 'r') as file:
            content = file.read()
            list = content.split(',')
            #print(list)
            return list

    def count_elements(self, array, target):
        array = np.array(array)
        return np.count_nonzero(array == target)  #用于数数据的数量

    def create_piechart(self, son_signal1):
        # 创建QPieSeries对象，它用来存放饼图的数据
        #print(zhanghao_now)
        #print(son_signal1)
        list = self.read_txt_audio()
        self.series = QPieSeries()

        # append方法中的数字，代表的是权重，完成可以改成其它，如80,70,60等等
        self.series.append("decorating", float(list[0]))
        self.series.append("other", float(list[1]))
        self.series.append("traffic", float(list[2]))
        # 单独处理某个扇区
        self.slice = QPieSlice()

        # 这里要处理的是python项，是依据前面append的顺序，如果是处理C++项的话，那索引就是3
        self.slice = self.series.slices()[0]  #得到饼图的一个切片

        # 突出显示，设置颜色
        self.slice.setExploded(True)
        self.slice.setLabelVisible(True)
        self.slice.setPen(QPen(Qt.red, 2))  #设置画笔类型
        self.slice.setBrush(Qt.red)  #设置笔刷

        # 创建QChart实例，它是PyQt5中的类
        self.chart = QChart()
        # QLegend类是显示图表的图例，先隐藏掉
        self.chart.legend().hide()
        self.chart.addSeries(self.series)  #将 pieseries添加到chart里
        self.chart.createDefaultAxes()
        self.chart.setTitle("the time")  #设置char的标题

        # 设置动画效果
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().setVisible(True)

        #设置背景透明
        self.chartview = QChartView(self.chart, self)
        self.chart.setBackgroundBrush(QBrush(QColor("transparent")))

        # 对齐方式
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # 创建ChartView，它是显示图表的控件
        #self.chartview = QChartView(self.chart,self)
        self.chartview.setRenderHint(QPainter.Antialiasing)
        self.chartview.setParent(self.ui.frame_4)  #需要设置父类，才能透明
        self.chartview.setGeometry(230, -20, 420, 300)  #设置charview在父窗口的大小、位置
        self.chartview.show()  #将CharView窗口显示出来

    def create_piechart_status(self, son_signal1):
        # 创建QPieSeries对象，它用来存放饼图的数
        #print(zhanghao_now)
        #print(son_signal1)
        list = status_list
        print(list)
        if (son_signal1 == 0):
            self.ui.status_label.setText('Now:    Computer')
        elif (son_signal1 == 1):
            self.ui.status_label.setText('Now:    phone')
        elif (son_signal1 == 2):
            self.ui.status_label.setText('Now:     book')
        elif (son_signal1 == 3):
            self.ui.status_label.setText('Now:     left')
        self.series = QPieSeries()

        computer = self.count_elements(list, 0)
        phone = self.count_elements(list, 1)
        book = self.count_elements(list, 2)
        left = self.count_elements(list, 3)

        study_count = round(
            ((computer + book) / (computer + phone + book + left)) * 100, 1)
        rest_count = round(100 - study_count, 1)
        self.ui.study_data.setText(str(study_count) + '%')
        self.ui.rest_data.setText(str(rest_count) + '%')

        # append方法中的数字，代表的是权重，完成可以改成其它，如80,70,60等等
        self.series.append("computer", computer)
        self.series.append("phone", phone)
        self.series.append("book", book)
        self.series.append("left", left)
        # 单独处理某个扇区
        self.slice = QPieSlice()

        # 这里要处理的是python项，是依据前面append的顺序，如果是处理C++项的话，那索引就是3
        self.slice = self.series.slices()[0]  #得到饼图的一个切片

        # 突出显示，设置颜色
        self.slice.setExploded(True)
        self.slice.setLabelVisible(True)
        self.slice.setPen(QPen(Qt.red, 2))  #设置画笔类型
        self.slice.setBrush(Qt.red)  #设置笔刷

        # 创建QChart实例，它是PyQt5中的类
        self.chart = QChart()
        # QLegend类是显示图表的图例，先隐藏掉
        self.chart.legend().hide()
        self.chart.addSeries(self.series)  #将 pieseries添加到chart里
        self.chart.createDefaultAxes()
        #self.chart.setTitle("the time")#设置char的标题

        # 设置动画效果
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        #设置背景透明
        self.chart.setBackgroundBrush(QBrush(QColor("transparent")))
        self.chart.legend().setVisible(True)

        # 对齐方式
        self.chart.legend().setAlignment(Qt.AlignRight)

        # 创建ChartView，它是显示图表的控件
        self.chartview = QChartView(self.chart, self)
        self.chartview.setRenderHint(QPainter.Antialiasing)  #抗锯齿
        self.chartview.setParent(self.ui.frame_4)  #需要设置父类，才能透明
        self.chartview.setGeometry(-40, -40, 350, 300)  #设置charview在父窗口的大小、位置

        self.chartview.show()  #将CharView窗口显示出来


class Son_thread_data_rec(QThread):
    # 定义一个信号，用于向主线程传递一个int型的变量
    son_signal1 = pyqtSignal(int)

    def __init__(self, my_run1):
        super(QThread, self).__init__()  #初始化类：QThread
        super(Son_thread_data_rec, self).__init__()  #初始化类：Son_Thread1
        #QTimer.singleShot(6000,self.print)
        self.my_run1 = my_run1

    def read_txt(self):
        with open('audio_classfication.txt', 'r') as file:
            self.content = file.read()
            print(self.content)

    def txt_update(self):  #模拟声音的产生事件
        with open('AudioClassification/audio_classfication.txt', 'w') as file:  #会覆盖
            str1 = str(random.uniform(0, 1))  #获取一个12~33之间的浮点数)
            str2 = str(random.uniform(0, 1))
            str3 = str(random.uniform(0, 1))
            file.write(str1 + ',' + str2 + ',' + str3)

    def txt_update_status(self):  #模拟现在学习状态的情况
        with open('status_classfication.txt', 'a') as file:  #追加指令
            str1 = 'SVMImageClassification/test_photo/output_image_1.png:'
            str2 = str(random.randint(0, 3))

            file.write(str1 + str2 + '\n')

    def txt_read_status(self):
        with open('SVMImageClassification/classification_results.txt',
                  'r') as file:
            self.content = file.read()
            self.content = self.content.splitlines()
            self.content_now = self.content[len(self.content) - 1]  #取出新增加的一行
            self.status = int(self.content_now[len(self.content_now) -
                                               1])  #取出现在的状态

            global status_list
            status_list.append(self.status)
            return self.status
            #print(status_list)

    def run(self):
        # while (1):
        #     #print(zhanghao_now)
        #     time.sleep(2)
        #     #self.read_txt()

        #     #self.txt_update()
        #     self.txt_update_status()
        #     self.txt_read_status()
        #     self.num = self.status
        #     self.son_signal1.emit(self.num)

        # lab host '192.168.124.7'
        # zrrraa host '192.168.43.226'
        self.run_classification_server('192.168.124.7', 8090)

    def run_classification_server(self, host, port):
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
        with open('SVMImageClassification/classification_results.txt',
                  'w') as f:
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
                received_data = client_socket.recv(1024).decode(
                    'utf-8')  # 以 UTF-8 解码接收客户端数据

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

                    # 更新到文件 "AudioClassification/audio_record.txt"
                    with open("AudioClassification/audio_record.txt",
                              'w') as file:
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
                    raw_bytes = np.array(
                        [int(x, 16) for x in HEXADECIMAL_BYTES], dtype="i2")

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

                    self.classify_images(output_path)

                    file_count += 1  # 增加文件计数器以便下一个文件

                    data = ""  # 重置数据变量

                    self.txt_read_status()
                    self.num = self.status
                    self.son_signal1.emit(self.num)

            # 关闭与客户端的连接
            client_socket.close()

    def classify_images(self, image_paths):
        mpl.rcParams['font.sans-serif'] = ['KaiTi']
        mpl.rcParams['font.serif'] = ['KaiTi']

        X = []
        Y = []
        Z = []

        for i in range(0, 4):
            for f in os.listdir("SVMImageClassification/photo3/%s" % i):
                X.append("SVMImageClassification/photo3//" + str(i) + "//" +
                         str(f))
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
            image = cv2.imdecode(np.fromfile(i, dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            img = cv2.resize(image, (256, 256), interpolation=cv2.INTER_CUBIC)
            hist = cv2.calcHist([img], [0, 1], None, [256, 256],
                                [0.0, 255.0, 0.0, 255.0])
            XX_train.append(((hist / 255).flatten()))

        XX_test = []
        for i in X_test:
            image = cv2.imdecode(np.fromfile(i, dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
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

        plot_confusion_matrix(cm_normalized,
                              title='Normalized confusion matrix')

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
        with open('SVMImageClassification/classification_results.txt',
                  'a') as f:
            for path, prediction in results:
                f.write(f'{path}: {prediction}\n')

        print('分类结果已保存到 classification_results.txt 文件中。')


if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 注意：需要加上这一行，自适应缩放，使实际显示效果和QTdesigner中保持一致
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    mylogin = MyloginForm()  #实例化
    mymain = MyMainForm()
    mysignup = MysignupForm()
    #将窗口控件显示在屏幕上
    mylogin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
