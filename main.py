from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QRegularExpressionValidator, QAction
from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu

import requests, json, os, asyncio, threading, time, subprocess, psutil

current_status = True  
process = None

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(558, 453)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 561, 141))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(False)
        font.setWeight(50)
        self.textBrowser.setFont(font)
        self.textBrowser.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.textBrowser.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(19, 149, 521, 211))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setFrame(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMaxLength(48)
        self.lineEdit.setPlaceholderText("1234567789:ABCDEFGHIJKLMNOPQRSTUVWXYZ012345678")
        self.verticalLayout_3.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.check_token)
        self.verticalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_3.setMaxLength(10)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setPlaceholderText("1122334455")
        self.verticalLayout_4.addWidget(self.lineEdit_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 380, 521, 51))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_4.setEnabled(True)
        self.pushButton_4.clicked.connect(self.save_data)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.windowIcon = QtGui.QIcon('icon.ico')
        MainWindow.setWindowIcon(self.windowIcon)
        
        regex = QRegularExpression("[0-9]+")
        validator = QRegularExpressionValidator(regex)
        self.lineEdit_3.setValidator(validator)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("tg-ctrl", "tg-ctrl"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt; font-weight:600; color:#5555ff;\">tg-ctrl</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Enter bot token (@BotFather)"))
        self.pushButton.setText(_translate("MainWindow", "Check"))
        self.label_3.setText(_translate("MainWindow", "Enter your Telegram ID (@id_users_bot)"))
        self.pushButton_4.setText(_translate("MainWindow", "Start"))
        
    def check_token(self):
        token = self.lineEdit.text()
        
        if token == "":
            self.pushButton.setText("Empty token!")
            return
        
        try:
            self.pushButton.setText("Checking...")
            response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
            if response.status_code == 200:
                self.pushButton.setText("Token is valid!")
            else:
                self.pushButton.setText("Invalid token.")
        except requests.exceptions.RequestException:
            self.pushButton.setText(f"Error connecting to Telegram API")
            
    def save_data(self):
        token = self.lineEdit.text()
        telegram_id = self.lineEdit_3.text()
        config_data = {
            "bot_token": token,
            "telegram_id": telegram_id
        }
        
        if token == "":
            self.pushButton_4.setText("Empty token!")
            return
        elif telegram_id == "":
            self.pushButton_4.setText("Empty Telegram ID!")
            return

        try:
            with open("config.json", "w") as config_file:
                json.dump(config_data, config_file, indent=4)
                
            MainWindow.hide()
            self.ui = Ui_RunWindow()
            self.ui.setupUi(MainWindow)
            MainWindow.show()
        except IOError:
            self.textBrowser.setText("Error")
            
class Ui_RunWindow(object):  
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(561, 290)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 561, 141))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(False)
        font.setWeight(50)
        self.textBrowser.setFont(font)
        self.textBrowser.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.textBrowser.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
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
        self.pushButton_4.clicked.connect(self.change_status)
        self.verticalLayout_5.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_5.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
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
        self.pushButton_5.clicked.connect(self.edit_settings)
        self.verticalLayout_5.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_6.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("")
        self.pushButton_6.setFlat(False)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_5.addWidget(self.pushButton_6)
        self.pushButton_6.clicked.connect(self.close_event)
        MainWindow.setCentralWidget(self.centralwidget)
        self.windowIcon = QtGui.QIcon('icon.ico')
        MainWindow.setWindowIcon(self.windowIcon)
        
        MainWindow.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)
        
        self.start_bot()
        
        tray = QSystemTrayIcon(app)
        tray.setIcon(QtGui.QIcon('icon.ico'))
        tray.setVisible(True)
            
        menu = QMenu()
        
        self.open_app = QAction("Open")
        self.open_app.triggered.connect(MainWindow.show)
        menu.addAction(self.open_app)
        
        if current_status:
            self.change_status = QAction("Stop")
        else:
            self.change_status = QAction("Start")     
            
        self.change_status.triggered.connect(self.change_tray_status)
        menu.addAction(self.change_status)
        
        menu.addSeparator()
            
        self.quit = QAction("Quit")
        self.quit.triggered.connect(self.stop)
        menu.addAction(self.quit)

        tray.setContextMenu(menu)
        
        self.update_button_text()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        global current_status
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "tg-ctrl"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt; font-weight:600; color:#5555ff;\">tg-ctrl</span></p></body></html>"))
        if current_status:
            self.pushButton_4.setText(_translate("MainWindow", "Stop"))
        else:
            self.pushButton_4.setText(_translate("MainWindow", "Start"))
        self.pushButton_5.setText(_translate("MainWindow", "Edit Settings"))
        self.pushButton_6.setText(_translate("MainWindow", "Minimize to tray"))
        
    def edit_settings(self):
        MainWindow.hide()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        MainWindow.show()     
        
    def close_event(self):
        MainWindow.hide()          
        
    def change_status(self):
        global current_status
        current_status = not current_status
        if current_status:
            self.pushButton_4.setText("Stop")
            self.start_bot()
        else:
            self.pushButton_4.setText("Start")
            self.stop_bot()
            
        self.update_tray_status()
            
    def update_button_text(self):
        global current_status
        self.pushButton_4.setText("Stop" if current_status else "Start")   
        
    def update_tray_status(self):
        if current_status:
            self.change_status.setText("Stop")
            self.start_bot()
        else:
            self.change_status.setText("Start")  
            self.stop_bot() 
            
    def change_tray_status(self):
        global current_status
        current_status = not current_status
        self.update_tray_status()
        MainWindow.hide() 
        self.update_button_text()    
        
    def bot(self):
        try:
            self.process = subprocess.Popen(
                ["bot.exe"],
                creationflags=subprocess.CREATE_NO_WINDOW
            )    
        except Exception:
            os.system(".\\build.bat")   
            
    def start_bot(self):
        with open("config.json", "r") as config_file:
                config_data = json.load(config_file)
                telegram_id = config_data["telegram_id"]
                token = config_data["bot_token"]
        
        if current_status:
            payload = {
                    "chat_id": telegram_id,
                    "text": "Client online ✅"
                }
            try:
                requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json=payload)
            except requests.exceptions.RequestException:
                pass   
            
        self.bot()
            
    def stop_bot(self):
        with open("config.json", "r") as config_file:
                config_data = json.load(config_file)
                telegram_id = config_data["telegram_id"]
                token = config_data["bot_token"]
        
        if not current_status:
            payload = {
                    "chat_id": telegram_id,
                    "text": "Client offline ❌"
            }
            try:
                requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json=payload)
            except requests.exceptions.RequestException:
                pass  
            
        try:
            for proc in psutil.process_iter():
                if proc.name() == 'bot.exe':
                    proc.kill() 
        except Exception:
            pass 
            
    def stop(self): 
        with open("config.json", "r") as config_file:
                config_data = json.load(config_file)
                telegram_id = config_data["telegram_id"]
                token = config_data["bot_token"]
        
        payload = {
                    "chat_id": telegram_id,
                    "text": "tg-ctrl closed ❌"
        }
        try:
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json=payload)
        except requests.exceptions.RequestException:
            pass  
        
        try:
            for proc in psutil.process_iter():
                if proc.name() == 'bot.exe':
                    proc.kill() 
        except Exception:
            pass
        
        os._exit(0)                  
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.ico'))
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowIcon(QtGui.QIcon('icon.ico'))
    
    if os.path.exists("config.json"):
        ui = Ui_RunWindow()
        ui.setupUi(MainWindow)
        if len(sys.argv) > 1 and sys.argv[1] == "--silent":
            pass
        else:
            MainWindow.show()
    else:
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()        
        
    sys.exit(app.exec())