# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'signup.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_signup(object):
    def setupUi(self, signup):
        signup.setObjectName("signup")
        signup.resize(1200, 800)
        self.zhanghao = QtWidgets.QLineEdit(signup)
        self.zhanghao.setGeometry(QtCore.QRect(540, 319, 171, 31))
        self.zhanghao.setObjectName("zhanghao")
        self.mima = QtWidgets.QLineEdit(signup)
        self.mima.setGeometry(QtCore.QRect(540, 369, 171, 31))
        self.mima.setObjectName("mima")
        self.querenmima = QtWidgets.QLineEdit(signup)
        self.querenmima.setGeometry(QtCore.QRect(540, 419, 171, 31))
        self.querenmima.setObjectName("querenmima")
        self.sign_up_button = QtWidgets.QPushButton(signup)
        self.sign_up_button.setGeometry(QtCore.QRect(420, 490, 301, 51))
        font = QtGui.QFont()
        font.setBold(True)
        self.sign_up_button.setFont(font)
        self.sign_up_button.setObjectName("sign_up_button")
        self.back_button = QtWidgets.QPushButton(signup)
        self.back_button.setGeometry(QtCore.QRect(420, 560, 301, 51))
        font = QtGui.QFont()
        font.setBold(True)
        self.back_button.setFont(font)
        self.back_button.setObjectName("back_button")
        self.label = QtWidgets.QLabel(signup)
        self.label.setGeometry(QtCore.QRect(420, 310, 101, 41))
        font = QtGui.QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(signup)
        self.label_2.setGeometry(QtCore.QRect(420, 370, 101, 31))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(signup)
        self.label_3.setGeometry(QtCore.QRect(420, 420, 101, 51))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(signup)
        self.label_4.setGeometry(QtCore.QRect(300, 150, 600, 500))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.thelogo = QtWidgets.QLabel(signup)
        self.thelogo.setGeometry(QtCore.QRect(310, 220, 141, 91))
        self.thelogo.setText("")
        self.thelogo.setObjectName("thelogo")
        self.label_5 = QtWidgets.QLabel(signup)
        self.label_5.setGeometry(QtCore.QRect(500, 200, 201, 81))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_4.raise_()
        self.zhanghao.raise_()
        self.mima.raise_()
        self.querenmima.raise_()
        self.sign_up_button.raise_()
        self.back_button.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.thelogo.raise_()
        self.label_5.raise_()

        self.retranslateUi(signup)
        QtCore.QMetaObject.connectSlotsByName(signup)

    def retranslateUi(self, signup):
        _translate = QtCore.QCoreApplication.translate
        signup.setWindowTitle(_translate("signup", "注册"))
        self.sign_up_button.setText(_translate("signup", "注册"))
        self.back_button.setText(_translate("signup", "退出"))
        self.label.setText(_translate("signup", "账号"))
        self.label_2.setText(_translate("signup", "密码"))
        self.label_3.setText(_translate("signup", "确认密码"))
