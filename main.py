from tkinter import *
from PIL import ImageTk, Image
# import numpy as np
# import tkinter as tk
# import client
import customtkinter
import cv2
import threading
import imutils
import pickle
import socket
import struct


def light_on_or_off():
    if L2['bg'] == '#ffffff':
        L2['bg'] = '#272727'
    else:
        L2['bg'] = '#ffffff'


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry('1300x814+79+0')
root.title('Video call')
root.resizable(0, 0)  # type: ignore

# img screen section
screen_frame = customtkinter.CTkFrame(master=root, corner_radius=9, width=1290, height=730, bg_color="#222222")
screen_frame.place(x=5, y=5)
L1 = Label(screen_frame, borderwidth=0, width=1280, height=720, bg="#272727")
L1.place(y=2, x=3)
# L1 = Label(screen_frame, borderwidth=0, width=183, height=48, bg="#9900ff")
# L1.place(y=2, x=3)

L2 = Label(root, borderwidth=0, width=183, height=3, bg="#272727")
L2.place(y=7, x=8)

setting_set = Frame(root, borderwidth=0, width=1290, height=66, bg="#222222", relief=GROOVE)
setting_set.place(y=740, x=0)

# setting_set
main_set = Frame(setting_set, borderwidth=0, width=200, height=76, bg="#222222", relief=GROOVE)
main_set.place(y=0, x=0)

btn_set = Frame(setting_set, borderwidth=0, width=200, height=76, bg="#222222", relief=GROOVE)
btn_set.place(y=0, x=500)

chart_set = Frame(setting_set, borderwidth=0, width=300, height=76, bg="#222222", relief=GROOVE)
chart_set.place(y=0, x=1000)
# main_set 
invite = Button(main_set, width=5, height=3, text="invite")
invite.place(y=17, x=10)
record = Button(main_set, width=5, height=5, text="record")
record.place(y=17, x=60)
participents = Button(main_set, width=5, height=5, text="participants")
participents.place(y=17, x=110)
light_btn = Button(main_set, width=5, height=5, text="Light", command=light_on_or_off)
light_btn.place(y=17, x=160)

# btn_set
btn_voice = Button(btn_set, width=5, height=3, text="voice")
btn_voice.place(y=17, x=10)
btn_video = Button(btn_set, width=5, height=5, text="video")
btn_video.place(y=17, x=60)
btn_call = Button(btn_set, width=5, height=5, text="call")
btn_call.place(y=17, x=110)

# chart_set

btn_Chat = Button(chart_set, width=5, height=3, text="Chat")
btn_Chat.place(y=17, x=0)
btn_Share_screen = Button(chart_set, width=5, height=5, text="screen")
btn_Share_screen.place(y=17, x=50)
btn_Raise_hand = Button(chart_set, width=5, height=5, text="Rhand")
btn_Raise_hand.place(y=17, x=100)
btn_React = Button(chart_set, width=5, height=3, text="React")
btn_React.place(y=17, x=150)
btn_More = Button(chart_set, width=5, height=5, text="More")
btn_More.place(y=17, x=200)
try:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    fps = cap.get(cv2.CAP_PROP_FPS)
    r, frame = cap.read()
    Resolution = str(frame.shape[0]) + ' x ' + str(frame.shape[1])
    print('fps', fps)
    print('Resolution:', Resolution)
except Exception as a:
    print()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.0.104'  # paste your server ip address here
port = 9999
client_socket.connect((host_ip, port))  # a tuple
data = b""
payload_size = struct.calcsize("Q")


while True:
    # img = cap.read()[1]
    # img_final = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # scale_percent = 100
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # resized = cv2.resize(img_final, dim, interpolation=cv2.INTER_AREA)
    # img = ImageTk.PhotoImage(Image.fromarray(resized))
    #
    # L1['image'] = img
    # root.update()
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
cap.release()

root.mainloop()
