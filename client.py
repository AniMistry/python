# from vidstream import StreamingServer
# import threading
# from tkinter import *
#
# root = Tk()
# root.geometry('1300x814+79+0')
# root.title('Video call')
# client1 = StreamingServer('192.168.0.107', 9998)
# # client1.start_server()
# t = threading.Thread(target=client1.start_server)
# t.start()
# while input("") != 'STOP':
#     continue
#
#
# client1.stop_server()


# import cv2
# import zmq
# import base64
# import numpy as np
# import socket
#
#
# context = zmq.Context()
# footage_socket = context.socket(zmq.SUB)
# footage_socket.bind('tcp://*:5555')
# footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode_(''))
#
# while True:
#     try:
#         frame = footage_socket.recv_string()
#         img = base64.b64decode(frame)
#         npimg = np.fromstring(img, dtype=np.uint8)
#         source = cv2.imdecode(npimg, 1)
#         cv2.imshow("Stream", source)
#
#         cv2.waitKey(1)
#
#
#     except KeyboardInterrupt:
#         cv2.destroyAllWindows()
#         break


import cv2
import pickle
import socket
import struct
from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('Video call')
# root.resizable(0, 0)  # type: ignore

L1 = Label(root)
L1.pack()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.0.104'  # paste your server ip address here
port = 9999
client_socket.connect((host_ip, port))  # a tuple
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    # cv2.imshow("RECEIVING VIDEO", frame)
    img_final = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img_final))
    L1['image'] = img
    root.update()
client_socket.close()

root.mainloop()