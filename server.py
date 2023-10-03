# from vidstream import CameraClient
# from vidstream import ScreenShareClient
# from vidstream import VideoClient
# import threading
#
#
# sender = CameraClient('192.168.0.107', 9998)
# t = threading.Thread(target=sender.start_stream)
# t.start()
# while input("") != 'STOP':
#     continue
#
#
# sender.stop_stream()

# import socket
# import sys
# import cv2
# import pickle
# import numpy as np
#
# HOST = '192.168.0.107'
# PORT = 8089
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# s.bind((HOST, PORT))
#
# s.listen(10)
#
# conn, addr = s.accept()
#
# while True:
#     data = conn.recv(80)
#     print(sys.getsizeof(data))
#     frame = pickle.loads(data)
#     print(frame)
#     cv2.imshow('frame', frame)

#
# import base64
# import socket
# import cv2
# import zmq
#
#
#
# context = zmq.Context()
# footage_socket = context.socket(zmq.PUB)
# footage_socket.connect('tcp://localhost:5555')
#
#
# camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # init the camera
#
# while True:
#     try:
#         grabbed, frame = camera.read()  # grab the current frame
#         frame = cv2.resize(frame, (640, 480))  # resize the frame
#         encoded, buffer = cv2.imencode('.jpg', frame)
#         jpg_as_text = base64.b64encode(buffer)
#         footage_socket.send(jpg_as_text)
#
#
#
#     except KeyboardInterrupt:
#         camera.release()
#         cv2.destroyAllWindows()
#         break


import cv2
import imutils
import pickle
import socket
import struct

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '192.168.0.104'
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("LISTENING AT:", socket_address)
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:

        while (vid.isOpened()):
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)







