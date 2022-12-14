import socket
import threading
import time

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication
import main_ui

NICK = ''


class Communicate(QObject):
    closeApp = pyqtSignal()


class Start(QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super(Start, self).__init__()
        self.setupUi(self)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 5014))

        self.play.clicked.connect(self.play_cl)
        print('left butt')
        self.send.clicked.connect(self.write)

    def play_cl(self):
        print('clicked play')
        self.nickname = self.nick.text()
        self.numberr = self.number.text()
        s = set()
        print('a')
        for i in self.numberr:
            s.add(i)
        print('b')
        if not self.nickname:
            self.nick.setText('SOMETHING IS WRONG')
            print('c')

        elif len(self.numberr) != 4 or len(s) != 4:
            self.number.setText("SOMETHING IS WRONG")
            print('d')

        else:
            self.number.setEnabled(False)
            self.nick.setEnabled(False)
            self.play.setEnabled(False)
            self.receive_thread = threading.Thread(target=self.receive)
            self.receive_thread.start()
            self.lock = threading.Lock()
        self.play.clicked.connect(self.play_cl)

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                print(message)
                if message == 'NUMB':
                    self.client.send(self.number.text().encode('utf-8'))
                elif message == "NICK":
                    self.client.send(self.nick.text().encode('utf-8'))
                    NICK = self.nick.text()
                elif message == '1':
                    self.send.setEnabled(True)
                    self.text.setEnabled(True)
                    self.ans.setEnabled(True)
                elif message[:5] == 'USER1':
                    self.user1.setText(message.split()[1])
                    self.user2.setText(message.split()[2])
                    print(message.split()[1], NICK)
                    if message.split()[1] == NICK:
                        self.send.setEnabled(True)
                        self.text.setEnabled(True)
                        self.ans.setEnabled(True)
                elif message[:3] == 'WIN':
                    self.res.setText(message)
                    self.ans.setEnabled(False)
                    break

                else:
                    self.text.append(message)
            except:
                print('ERROR')
                self.text.append('Error!')
                self.client.close()
                break

    def write(self):
        message = '{}'.format(self.ans.text())
        self.ans.setText('')
        self.client.send(message.encode('utf-8'))
        self.ans.setEnabled(False)


if __name__ == '__main__':
    app = QApplication([])
    window = Start()
    window.show()
    app.exec()
