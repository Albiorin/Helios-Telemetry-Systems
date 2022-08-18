from re import S
import sys
from turtle import delay
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import socket
import struct
import pickle
import numpy as np
from queue import *
import PyQt5
import time
import keyboard

host = '10.20.50.87'
port = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 80))
queue = Queue()
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.VBL = QVBoxLayout()
        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)
        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)
        self.Worker2 = Worker1()
        self.Worker2.start()
        self.Worker1 = Worker2()
        self.Worker1.start()
        self.Worker3 = Worker3()
        self.Worker3.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
    def CancelFeed(self):
        print("hehe")

print("Main thread online")
class Worker1(QThread):
    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            print("Worker 2 online")
            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = s.recv(4*1024)
                    if not packet: break
                    data += packet
                    packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += s.recv(4*1024)
                frame_data = data[:msg_size] 
                data = data[msg_size:]
                packetframe = pickle.loads(frame_data)
                #time.sleep(0.01)
                queue.put(packetframe)
                #print(packetframe)
                key = cv2.waitKey(10)
                if key == 13:
                    break
            key = cv2.waitKey(10)
            if key == 13:
                break
    def stop(self):
        self.ThreadActive = False
        self.quit()

class Worker2(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            packetframe = queue.get()
            Image = cv2.cvtColor(packetframe, cv2.COLOR_BGR2RGB)
            ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888) 
            Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.ImageUpdate.emit(Pic)
            key = cv2.waitKey(10)
            if key == 13:
                break 
    def stop(self):
        self.ThreadActive = False
        self.quit()

class Worker3(QThread):
    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            while True:
                if keyboard.read_key() == "w":
                    print("Going Forward...")
                elif keyboard.read_key() == "s":
                    print("Reversing...")
                elif keyboard.read_key() == "a":
                    print("Turning left...")
                elif keyboard.read_key() == "d":
                    print("Turning right...")
                    break           
    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())