# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.setFixedSize(1152, 99)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.familiaBox = QtWidgets.QComboBox(Dialog)
        self.familiaBox.setGeometry(QtCore.QRect(10, 30, 131, 26))
        self.familiaBox.setObjectName("familiaBox")
        self.streetBox = QtWidgets.QComboBox(Dialog)
        self.streetBox.setGeometry(QtCore.QRect(660, 30, 141, 26))
        self.streetBox.setObjectName("streetBox")
        self.nameBox = QtWidgets.QComboBox(Dialog)
        self.nameBox.setGeometry(QtCore.QRect(170, 30, 131, 26))
        self.nameBox.setObjectName("nameBox")
        self.otcestvoBox = QtWidgets.QComboBox(Dialog)
        self.otcestvoBox.setGeometry(QtCore.QRect(330, 30, 131, 26))
        self.otcestvoBox.setObjectName("otcestvoBox")
        self.buildingBox = QtWidgets.QTextEdit(Dialog)
        self.buildingBox.setGeometry(QtCore.QRect(830, 30, 51, 21))
        self.buildingBox.setObjectName("buildingBox")
        self.famLabel = QtWidgets.QLabel(Dialog)
        self.famLabel.setGeometry(QtCore.QRect(10, 10, 60, 16))
        self.famLabel.setObjectName("famLabel")
        self.nameLabel = QtWidgets.QLabel(Dialog)
        self.nameLabel.setGeometry(QtCore.QRect(170, 10, 60, 16))
        self.nameLabel.setObjectName("nameLabel")
        self.otcLabel = QtWidgets.QLabel(Dialog)
        self.otcLabel.setGeometry(QtCore.QRect(330, 10, 60, 16))
        self.otcLabel.setObjectName("otcLabel")
        self.streetLabel = QtWidgets.QLabel(Dialog)
        self.streetLabel.setGeometry(QtCore.QRect(660, 10, 60, 16))
        self.streetLabel.setObjectName("streetLabel")
        self.bldnLabel = QtWidgets.QLabel(Dialog)
        self.bldnLabel.setGeometry(QtCore.QRect(830, 10, 60, 16))
        self.bldnLabel.setObjectName("bldnLabel")
        self.telLabel = QtWidgets.QLabel(Dialog)
        self.telLabel.setGeometry(QtCore.QRect(990, 10, 60, 16))
        self.telLabel.setObjectName("telLabel")
        self.corpBox = QtWidgets.QTextEdit(Dialog)
        self.corpBox.setGeometry(QtCore.QRect(910, 30, 51, 21))
        self.corpBox.setObjectName("corpBox")
        self.corpLabel = QtWidgets.QLabel(Dialog)
        self.corpLabel.setGeometry(QtCore.QRect(910, 10, 60, 16))
        self.corpLabel.setObjectName("corpLabel")
        self.cityBox = QtWidgets.QComboBox(Dialog)
        self.cityBox.setGeometry(QtCore.QRect(490, 30, 141, 26))
        self.cityBox.setObjectName("cityBox")
        self.citylabel = QtWidgets.QLabel(Dialog)
        self.citylabel.setGeometry(QtCore.QRect(490, 10, 60, 16))
        self.citylabel.setObjectName("citylabel")
        self.CloseButton = QtWidgets.QPushButton(Dialog)
        self.CloseButton.setGeometry(QtCore.QRect(920, 60, 113, 32))
        self.CloseButton.setObjectName("CloseButton")
        self.ChangeEntryButton = QtWidgets.QPushButton(Dialog)
        self.ChangeEntryButton.setGeometry(QtCore.QRect(1030, 60, 113, 32))
        self.ChangeEntryButton.setObjectName("ChangeEntryButton")
        self.telBox = QtWidgets.QTextEdit(Dialog)
        self.telBox.setGeometry(QtCore.QRect(990, 30, 151, 21))
        self.telBox.setObjectName("telBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Изменение"))
        self.famLabel.setText(_translate("Dialog", "Фамилия"))
        self.nameLabel.setText(_translate("Dialog", "Имя"))
        self.otcLabel.setText(_translate("Dialog", "Отчество"))
        self.streetLabel.setText(_translate("Dialog", "Улица"))
        self.bldnLabel.setText(_translate("Dialog", "Дом"))
        self.telLabel.setText(_translate("Dialog", "Телефон"))
        self.corpLabel.setText(_translate("Dialog", "Корпус"))
        self.citylabel.setText(_translate("Dialog", "Город"))
        self.CloseButton.setText(_translate("Dialog", "Отмена"))
        self.ChangeEntryButton.setText(_translate("Dialog", "Изменить"))
