import socket
import cv2
import pickle
import struct
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Welcome to Helios Ground Systems")
time.sleep(2)
host = input('Enter instrument ip address: ')
time.sleep(1)
print('Connecting...')
time.sleep(2)
port = 80
client_socket.connect((host, 80))
data = b""

payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size] 
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("Client", frame)
    key = cv2.waitKey(10)
    if key == 13:
        break
client_socket.close()
