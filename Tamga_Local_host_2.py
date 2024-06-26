# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Tamga.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import QThread
import socket
import sys
import ssl
import threading
import time
from cryptography.fernet import Fernet
from vigenere_method import vigenere_encrption, vigenere_decryption


class Communicate(QObject):
    send_data = pyqtSignal(str)
    update_ip = pyqtSignal(str)

class ServerIpThread(QThread):
    update_ip = pyqtSignal(str)

    def run(self):
        # Set up the broadcast socket to listen for IP addresses
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        broadcast_socket.bind(('0.0.0.0', 5556))

        while True:
            data, _ = broadcast_socket.recvfrom(1024)
            encrypted_ip = data
            print(f"Received Encrypted Data: {encrypted_ip}")
            print(f"Received Data Type: {type(encrypted_ip)}")

            if ui.secret_key is not None:
                try:
                    decrypted_ip = ui.fernet.decrypt(encrypted_ip).decode()
                    print(f"Decrypted IP: {decrypted_ip}")
                    self.update_ip.emit(decrypted_ip)

                    if ui.client_socket is not None:
                        ui.client_socket.close()

                    ui.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ui.client_socket.connect((decrypted_ip, 5555))

                    # Send a message to acknowledge connection
                    ui.client_socket.send("Connection established".encode())
                except Exception as e:
                    print(f"Error while decrypting: {e}")
            else:
                # First message received contains the secret key, set it up
                ui.secret_key = Fernet.generate_key()
                ui.fernet = Fernet(ui.secret_key)
                print("Fernet key initialized")

            # Add a small delay to avoid high CPU usage
            self.msleep(1000)


class Ui_MainWindow(object):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        # Initialize the thread
        self.thread = ServerIpThread()
        self.thread.update_ip.connect(self.update_server_ip)

        # Set up the UI
        self.init_ui()

        # Start the thread
        self.thread.start()

    def init_ui(self):
        self.communication = Communicate()

        # Start the thread
        self.thread.start()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(857, 285)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(60, 40, 771, 211))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.msj_label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.msj_label.sizePolicy().hasHeightForWidth())
        self.msj_label.setSizePolicy(sizePolicy)
        self.msj_label.setObjectName("msj_label")
        self.verticalLayout.addWidget(self.msj_label, 0, QtCore.Qt.AlignHCenter)

        self.msj_edit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.msj_edit.sizePolicy().hasHeightForWidth())
        self.msj_edit.setSizePolicy(sizePolicy)
        self.msj_edit.setObjectName("msj_edit")
        self.verticalLayout.addWidget(self.msj_edit)

        self.keyWord = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keyWord.sizePolicy().hasHeightForWidth())
        self.keyWord.setSizePolicy(sizePolicy)
        self.keyWord.setObjectName("keyWord")
        self.verticalLayout.addWidget(self.keyWord, 0, QtCore.Qt.AlignHCenter)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        self.Sender = QtWidgets.QPushButton(self.widget)
        self.Sender.setObjectName("Sender")
        self.verticalLayout.addWidget(self.Sender)

        self.cipher_sent = QtWidgets.QLabel(self.widget)
        self.cipher_sent.setObjectName("cipher_sent")
        self.verticalLayout.addWidget(self.cipher_sent, 0, QtCore.Qt.AlignHCenter)

        self.cipher_msj_sent = QtWidgets.QLabel(self.widget)
        self.cipher_msj_sent.setText("")
        self.cipher_msj_sent.setObjectName("cipher_msj_sent")
        self.verticalLayout.addWidget(self.cipher_msj_sent, 0, QtCore.Qt.AlignHCenter)

        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.receive_label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.receive_label.sizePolicy().hasHeightForWidth())
        self.receive_label.setSizePolicy(sizePolicy)
        self.receive_label.setObjectName("receive_label")
        self.verticalLayout_2.addWidget(self.receive_label, 0, QtCore.Qt.AlignHCenter)

        self.received_msj = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.received_msj.sizePolicy().hasHeightForWidth())
        self.received_msj.setSizePolicy(sizePolicy)
        self.received_msj.setText("")
        self.received_msj.setObjectName("received_msj")
        self.verticalLayout_2.addWidget(self.received_msj, 0, QtCore.Qt.AlignHCenter)

        self.KeyWord_receieve = QtWidgets.QLabel(self.widget)
        self.KeyWord_receieve.setObjectName("KeyWord_receieve")
        self.verticalLayout_2.addWidget(self.KeyWord_receieve, 0, QtCore.Qt.AlignHCenter)

        self.KeyWord_receieve_txt = QtWidgets.QLineEdit(self.widget)
        self.KeyWord_receieve_txt.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.KeyWord_receieve_txt)

        self.decipher_button = QtWidgets.QPushButton(self.widget)
        self.decipher_button.setObjectName("decipher_button")
        self.verticalLayout_2.addWidget(self.decipher_button)

        self.cipher_label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cipher_label.sizePolicy().hasHeightForWidth())
        self.cipher_label.setSizePolicy(sizePolicy)
        self.cipher_label.setObjectName("cipher_label")
        self.verticalLayout_2.addWidget(self.cipher_label, 0, QtCore.Qt.AlignHCenter)

        self.decipher_msj = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.decipher_msj.sizePolicy().hasHeightForWidth())
        self.decipher_msj.setSizePolicy(sizePolicy)
        self.decipher_msj.setText("")
        self.decipher_msj.setObjectName("decipher_msj")
        self.verticalLayout_2.addWidget(self.decipher_msj, 0, QtCore.Qt.AlignHCenter)

        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.ip_label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ip_label.sizePolicy().hasHeightForWidth())
        self.ip_label.setSizePolicy(sizePolicy)
        self.ip_label.setText("")
        self.ip_label.setObjectName("ip_label")
        self.horizontalLayout.addWidget(self.ip_label, 0, QtCore.Qt.AlignHCenter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.msj_label.setText(_translate("MainWindow", "Gönderilecek Mesajı Giriniz"))
        self.keyWord.setText(_translate("MainWindow", "Anahtar Kelimeyi giriniz"))
        self.Sender.setText(_translate("MainWindow", "GÖNDER"))
        self.Sender.clicked.connect(self.send_data_to_first_program)
        self.cipher_sent.setText(_translate("MainWindow", "Gönderilen Şifreli Mesaj"))
        self.receive_label.setText(_translate("MainWindow", "Gelen Şifreli Mesaj"))
        self.KeyWord_receieve.setText(_translate("MainWindow", "Anahtar kelimeyi giriniz"))
        self.decipher_button.setText(_translate("MainWindow", "Şifreyi Çöz"))
        self.decipher_button.clicked.connect(self.receiving_msj)
        self.cipher_label.setText(_translate("MainWindow", "Gelen Çözülmüş Mesaj"))

        self.communication.send_data.connect(self.receive_data_from_first_program)
        self.communication.update_ip.connect(self.update_server_ip)

        self.secret_key = None
        self.fernet = None
        self.client_socket = None

    def receiving_msj(self):
        data = ""
        data = self.received_msj.text()
        keyword_data = self.KeyWord_receieve_txt.text()
        if keyword_data != "" and data != "":
            self.decipher_msj.setText(vigenere_decryption(data, keyword_data))
        else:
            self.decipher_msj.setText("$$forget the keyword$$")

    def start_listening_for_server_ip(self):
        # Set up the broadcast socket to listen for IP addresses
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        broadcast_socket.bind(('0.0.0.0', 5556))

        while True:
            data, _ = broadcast_socket.recvfrom(1024)
            encrypted_ip = data
            if self.secret_key is not None:
                decrypted_ip = self.fernet.decrypt(encrypted_ip).decode()
                self.communication.update_ip.emit(decrypted_ip)

                if self.client_socket is not None:
                    self.client_socket.close()

                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((decrypted_ip, 5555))

                # Send a message to acknowledge connection
                self.client_socket.send("Connection established".encode())
            else:
                # First message received contains the secret key, set it up
                self.secret_key = Fernet.generate_key()
                self.fernet = Fernet(self.secret_key)

    def receive_data_from_first_program(self, data):
        self.received_msj.setText(f'Received Data: {data}')

    def send_data_to_first_program(self):
        data = self.msj_label.text()
        self.communication.send_data.emit(data)
        self.client_socket.send(data.encode())
        received_data = self.client_socket.recv(1024).decode()  # Receive data from the first program
        print(f'Received Data from First Program: {received_data}')

    def update_server_ip(self, ip):
        self.ip_label.setText(f'Server IP: {ip}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    # Start the application
    MainWindow.show()

    sys.exit(app.exec_())
