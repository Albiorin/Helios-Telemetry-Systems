from http import client
import socket
import cv2
import pickle
import struct
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from qt_thread_updater import ThreadUpdater
from queue import *
import sys

host = 'localhost'
port = 80
queue = Queue()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
server_socket.bind((host, 80))
print('Socket bind complete')
server_socket.listen(10)
print('Socket listening on port 80')

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker2 = Worker2()
        self.Worker2.start()

def __draw_label(img, text, pos, bg_color):
   font_face = cv2.FONT_HERSHEY_SIMPLEX
   scale = 0.4
   color = (0, 0, 0)
   thickness = cv2.FILLED
   margin = 2
   txt_size = cv2.getTextSize(text, font_face, scale, thickness)
   end_x = pos[0] + txt_size[0][0] + margin
   end_y = pos[1] - txt_size[0][1] - margin
   cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
   cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)

class Worker1(QThread):
    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            while True:
                client_socket,addr = server_socket.accept()
                queue.put(client_socket)
                print('Connection from:' ,addr)
                if client_socket:
                    vid = cv2.VideoCapture(0)
                    while(vid.isOpened()):
                        img, frame = vid.read()
                        #__draw_label(frame, 'Hello World', (20,20), (255,0,0))
                        a = pickle.dumps(frame)
                        message = struct.pack("Q", len(a))+a
                        client_socket.sendall(message)
                        key = cv2.waitKey(10)
                        if key == 13:
                            client_socket.close()
        def stop(self):
            self.ThreadActive = False
            self.quit()

class Worker2(QThread):
    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            client_socket = queue.get()
            while True:
                dataFromClient = client_socket.recv(1024)

                if dataFromClient == b'forward':
                    print("forward command recieved")
                    #send b'forward' to motor controllers

                elif dataFromClient == b'reverse':
                    print("reverse command recieved")
                    #send b'reverse' to motor controllers

                elif dataFromClient == b'left':
                    print("left command recieved")
                    #send b'left' to motor controllers

                elif dataFromClient == b'right':
                    print("right command recieved")
                    #send b'right' to motor controllers

                key = cv2.waitKey(10)
                if key == 13:
                    break
    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    sys.exit(App.exec())