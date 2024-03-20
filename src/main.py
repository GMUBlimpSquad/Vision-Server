#!/usr/bin/env python

import socket
import cv2 as cv
import struct
import numpy as np
from ultralytics import YOLO
from _thread import start_new_thread
import torch


HOST = "0.0.0.0"
PORT = 4000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()



frameSize = 0
#model = torch.hub.load("model/best.pt")
model = YOLO('model/best.pt')


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
            #cv.imwrite("image.png",img)
            #cv.imshow("image", img)
            results = model(img, conf=0.8)
            #for r in results:
                #r.save()
              #  print(r.boxes.xywh)
            #print(results)
            coor = results[0].boxes.xywh
            xywh = torch.tensor(coor).tolist()
            print(xywh)
            if len(xywh) > 0:
                coor_arr = [int(x) for x in xywh[0]]
                sendstr = str(coor_arr)[1:len(str(coor_arr))-1] + "#"
                print(coor_arr)
                #cv.rectangle(img,(coor_arr[0], coor_arr[1]), ( coor_arr[2], coor_arr[3]), (0,255,0), 3)
                conn.send(sendstr.encode('utf-8'))
            #results.show()
            else:
                conn.send("0,0,0,0,0,0#".encode('utf-8'))


        else:
            print("Bad frame recv")

    conn.close()

try:
    while (True):
        conn, addr = s.accept()
        start_new_thread(on_new_client, (conn,addr))

except KeyboardInterrupt:
    s.close()
