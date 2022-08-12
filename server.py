import socket
import cv2
import pickle
import struct

host = '169.254.42.82'
port = 80

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

server_socket.bind((host, 80))
print('Socket bind complete')

server_socket.listen(10)
print('Socket listening on port 80')

while True:
    client_socket,addr = server_socket.accept()
    print('Connection from:' ,addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        while(vid.isOpened()):
            img, frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a))+a
            client_socket.sendall(message)
            cv2.imshow('Server',frame)
            key = cv2.waitKey(10)
            if key == 13:
                client_socket.close()