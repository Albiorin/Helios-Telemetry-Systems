import socket
import cv2
import pickle
import struct

host = '10.20.50.87'
port = 80
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
server_socket.bind((host, 80))
print('Socket bind complete')
server_socket.listen(10)
print('Socket listening on port 80')

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

while True:
    client_socket,addr = server_socket.accept()
    print('Connection from:' ,addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        while(vid.isOpened()):
            img, frame = vid.read()
            __draw_label(frame, 'Hello World', (20,20), (255,0,0))
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a))+a
            client_socket.sendall(message)
            key = cv2.waitKey(10)
            if key == 13:
                client_socket.close()