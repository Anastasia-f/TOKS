# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Lab3.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(700, 760)
        MainWindow.setMinimumSize(QSize(700, 760))
        MainWindow.setMaximumSize(QSize(700, 760))
        MainWindow.setMouseTracking(False)
        MainWindow.setTabletTracking(False)
        MainWindow.setStyleSheet(u"background-color: rgb(244, 255, 246);\n"
"\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.InputGroupBox = QGroupBox(self.centralwidget)
        self.InputGroupBox.setObjectName(u"InputGroupBox")
        self.InputGroupBox.setMinimumSize(QSize(670, 140))
        self.InputGroupBox.setMaximumSize(QSize(670, 130))
        self.InputGroupBox.setStyleSheet(u"background-color: rgb(244, 255, 246);")
        self.InputMessage = QTextEdit(self.InputGroupBox)
        self.InputMessage.setObjectName(u"InputMessage")
        self.InputMessage.setGeometry(QRect(10, 30, 650, 100))
        self.InputMessage.setMinimumSize(QSize(650, 0))
        self.InputMessage.setMaximumSize(QSize(650, 16777215))
        self.InputMessage.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.InputMessage.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.InputMessage.setTextInteractionFlags(Qt.TextEditorInteraction)

        self.verticalLayout_2.addWidget(self.InputGroupBox)

        self.OutputGroupBox = QGroupBox(self.centralwidget)
        self.OutputGroupBox.setObjectName(u"OutputGroupBox")
        self.OutputGroupBox.setMinimumSize(QSize(670, 220))
        self.OutputGroupBox.setMaximumSize(QSize(670, 200))
        self.OutputGroupBox.setStyleSheet(u"background-color: rgb(244, 255, 246);\n"
"")
        self.OutputMessage = QTextEdit(self.OutputGroupBox)
        self.OutputMessage.setObjectName(u"OutputMessage")
        self.OutputMessage.setGeometry(QRect(10, 30, 650, 170))
        self.OutputMessage.setMinimumSize(QSize(650, 170))
        self.OutputMessage.setMaximumSize(QSize(650, 170))
        self.OutputMessage.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.OutputMessage.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.OutputMessage.setReadOnly(True)
        self.OutputMessage.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.verticalLayout_2.addWidget(self.OutputGroupBox)

        self.CDGroupBox = QGroupBox(self.centralwidget)
        self.CDGroupBox.setObjectName(u"CDGroupBox")
        self.CDGroupBox.setMinimumSize(QSize(670, 320))
        self.CDGroupBox.setMaximumSize(QSize(670, 320))
        self.CDGroupBox.setStyleSheet(u"background-color: rgb(244, 255, 246);\n"
"")
        self.CD_CB_PortSpeed = QComboBox(self.CDGroupBox)
        self.CD_CB_PortSpeed.addItem("")
        self.CD_CB_PortSpeed.addItem("")
        self.CD_CB_PortSpeed.addItem("")
        self.CD_CB_PortSpeed.addItem("")
        self.CD_CB_PortSpeed.addItem("")
        self.CD_CB_PortSpeed.addItem("")
        self.CD_CB_PortSpeed.addItem("")
        self.CD_CB_PortSpeed.addItem("")
        self.CD_CB_PortSpeed.addItem("")
        self.CD_CB_PortSpeed.setObjectName(u"CD_CB_PortSpeed")
        self.CD_CB_PortSpeed.setGeometry(QRect(10, 250, 165, 50))
        self.CD_CB_PortSpeed.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.CD_Message = QTextEdit(self.CDGroupBox)
        self.CD_Message.setObjectName(u"CD_Message")
        self.CD_Message.setGeometry(QRect(10, 30, 650, 170))
        self.CD_Message.setMinimumSize(QSize(650, 0))
        self.CD_Message.setMaximumSize(QSize(650, 170))
        self.CD_Message.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.CD_Message.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.CD_Message.setReadOnly(True)
        self.CD_Message.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.CD_BtnClear = QPushButton(self.CDGroupBox)
        self.CD_BtnClear.setObjectName(u"CD_BtnClear")
        self.CD_BtnClear.setGeometry(QRect(220, 250, 190, 50))
        self.CD_BtnClear.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.OutputBtnClear = QPushButton(self.CDGroupBox)
        self.OutputBtnClear.setObjectName(u"OutputBtnClear")
        self.OutputBtnClear.setGeometry(QRect(470, 250, 190, 50))
        self.OutputBtnClear.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_2 = QLabel(self.CDGroupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 200, 161, 61))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setLayoutDirection(Qt.LeftToRight)
        self.label_2.raise_()
        self.CD_CB_PortSpeed.raise_()
        self.CD_BtnClear.raise_()
        self.CD_Message.raise_()
        self.OutputBtnClear.raise_()

        self.verticalLayout_2.addWidget(self.CDGroupBox)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.CD_CB_PortSpeed.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Lab3", None))
        self.InputGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u043e\u0434", None))
        self.OutputGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0432\u043e\u0434", None))
        self.CDGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043d\u0442\u0440\u043e\u043b\u044c \u0438 \u041b\u043e\u0433\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.CD_CB_PortSpeed.setItemText(0, QCoreApplication.translate("MainWindow", u"1200", None))
        self.CD_CB_PortSpeed.setItemText(1, QCoreApplication.translate("MainWindow", u"1800", None))
        self.CD_CB_PortSpeed.setItemText(2, QCoreApplication.translate("MainWindow", u"2400", None))
        self.CD_CB_PortSpeed.setItemText(3, QCoreApplication.translate("MainWindow", u"4800", None))
        self.CD_CB_PortSpeed.setItemText(4, QCoreApplication.translate("MainWindow", u"9600", None))
        self.CD_CB_PortSpeed.setItemText(5, QCoreApplication.translate("MainWindow", u"19200", None))
        self.CD_CB_PortSpeed.setItemText(6, QCoreApplication.translate("MainWindow", u"38400", None))
        self.CD_CB_PortSpeed.setItemText(7, QCoreApplication.translate("MainWindow", u"57600", None))
        self.CD_CB_PortSpeed.setItemText(8, QCoreApplication.translate("MainWindow", u"115200", None))

        self.CD_BtnClear.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u041a\u041b", None))
        self.OutputBtnClear.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0432\u044b\u0432\u043e\u0434", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u043f\u043e\u0440\u0442\u0430</p></body></html>", None))
    # retranslateUi

