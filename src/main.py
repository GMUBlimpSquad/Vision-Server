#!/usr/bin/env python

import socket
import cv2 as cv
import struct
import numpy as np
import torch


HOST = "0.0.0.0"
PORT = 8000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

frameSize = 0
model = torch.hub.load("ultralytics/yolov5", 'custom', path="model/best.pt", force_reload=True)


def on_new_client(conn, addr):
    print("Connected to ",addr)
    while True:
        header = conn.recv(4)
        try:
            bytes_to_read = int(header.decode())
        except:
            bytes_to_read = 0
        img = bytes()
        #print(bytes_to_read)
        while len(img) < bytes_to_read:
            img += conn.recv(min(bytes_to_read - len(img), 4096))

        if len(img) >4:
            img = np.frombuffer(img, np.uint8)

            img = cv.imdecode(img, cv.IMREAD_COLOR)
            cv.imwrite("image.png",img)

            results = model(img)
            coor = results.xyxy[0]
            xywh = torch.tensor(coor).tolist()
            if len(xywh) > 0:
                coor_arr = [int(x) for x in xywh[0]]
                sendstr = str(coor_arr)[1:len(str(coor_arr))-1] + "#"
                print(coor_arr)
                cv.rectangle(img,(coor_arr[0], coor_arr[1]), ( coor_arr[2], coor_arr[3]), (0,255,0), 3)
                conn.send(sendstr.encode('utf-8'))
            # results.show()
            # cv.imshow("image", img)
        else:
            print("Bad frame recv")

    conn.close()




try:
    while (True):
        conn, addr = s.accept()
        thread.start_new_thread(on_new_client, (c,addr))

except KeyboardInterrupt:
    s.close()
