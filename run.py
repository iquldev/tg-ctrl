from PyQt5 import QtCore, QtGui, QtWidgets
from main import Ui_MainWindow

class Ui_RunWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(561, 291)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 561, 141))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(False)
        font.setWeight(50)
        self.textBrowser.setFont(font)
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 160, 521, 111))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_4.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("")
        self.pushButton_4.setFlat(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_5.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_5.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("")
        self.pushButton_5.setFlat(False)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_5.addWidget(self.pushButton_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.windowIcon = QtGui.QIcon('icon.png')
        MainWindow.setWindowIcon(self.windowIcon)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "tg-ctrl"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt; font-weight:600; color:#5555ff;\">tg-ctrl</span></p></body></html>"))
        self.pushButton_4.setText(_translate("MainWindow", "Start"))
        self.pushButton_5.setText(_translate("MainWindow", "Edit Settings"))
        
    def edit_settings(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()