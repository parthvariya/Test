import cv2
import numpy as np
from multiprocessing import Process
#from joystick import get_data_for_gui

#
def receive():
    #video pipeline
    cap_receive = cv2.VideoCapture('udpsrc port=19295 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
    if not cap_receive.isOpened():
        print('VideoCapture not opened')
        exit(0)

    while True:
        ret,frame = cap_receive.read()

        if not ret:
            print('empty frame')
            break

        cv2.imshow('receive', frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break

def receive_back():
    frame = np.zeros((200,900,3), dtype = np.uint8)
    cv2.imshow('back', frame) 


# start GUI    
def receive_video_from_car():    
     # Create a window and pass it to the Application object
     receive()
     
#def receive_video_from_car_rear():    
     #Create a window and pass it to the Application object
     #receive_back()