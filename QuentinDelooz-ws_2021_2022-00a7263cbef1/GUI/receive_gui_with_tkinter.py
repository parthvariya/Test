#receiver file - needs to be optimised due to delay in GUI

import tkinter
from PIL import Image, ImageTk
import cv2
import numpy as np
from multiprocessing import Process
#from joystick import get_data_for_gui
from sd_teleop_control import get_data_for_gui

number_of_cameras = 2

(w, h) = (960*2*3, 1000) # Canvas size for 3 cameras together
(w_r,h_r) = (960,250) # Canvas size for rear view cameras
(w_d,h_d) = (600,600) #Canvas size for the data

class App:
    def __init__(self, window, window_title, video_source=0):
        # configure window
        self.window = window
        self.window.title(window_title)
        self.window.configure(bg='white')

        #video pipeline
        self.video_source = 'udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! appsink'

        # open video stream
        self.vid = MyVideoCapture(self.video_source)
        
        # configure GUI
        self.content = tkinter.Frame(window, bg='white')
        self.data = tkinter.Frame(window, bg='white')
        self.content.grid(row=7, column=0, columnspan=24)
        
        # Create a canvas that can fit the above video source size
        self.canvas = [None] * 3
        self.canvas[0] = tkinter.Canvas(window, width = w, height = h) #entire frame
        self.canvas[1] = tkinter.Canvas(window, width = w_r, height = h_r) #rear view canvas
        self.data=tkinter.Canvas(window, bg = 'white', width=w_d, height=h_d)

        # give GUI a structure
        self.canvas[0].grid(row=0, column=0,rowspan=8,columnspan=24) # entire frame
        self.canvas[1].grid(row=0, column=10,columnspan=4,rowspan=2) # rear view
        self.data.grid(row=7,column=8,columnspan=2,rowspan=2,sticky='s')
        
        # defining labels for data
        self.accel = tkinter.Label(self.data, justify=tkinter.LEFT,padx=25, font="Verdana 10", text="Acceleration:", bg='white')
        self.brake = tkinter.Label(self.data, justify=tkinter.LEFT,padx=25,font="Verdana 10", text="Braking:", bg='white')
        self.steer = tkinter.Label(self.data, justify=tkinter.LEFT, pady=10,font="Verdana 10", text="Steering Angle:", anchor=tkinter.E, bg='white')
        self.accel_in = tkinter.Label(self.data, justify=tkinter.LEFT,padx=25,font="Verdana 10", text="0.00", bg='white')
        self.steer_in = tkinter.Label(self.data, justify=tkinter.LEFT, padx=25,font="Verdana 10", text="0.00", bg='white')
        self.brake_in = tkinter.Label(self.data, justify=tkinter.LEFT, padx=25,font="Verdana 10", text="0.00", bg='white')

        # place labels on content frame
        self.accel.grid(row=0, column=0)
        self.steer.grid(row=1, column=0)
        self.accel_in.grid(row=0, column=1)
        self.steer_in.grid(row=1, column=1)
        self.brake.grid(row=2, column=0)
        self.brake_in.grid(row=2, column=1)
     
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        
        # init further variables
        self.photo = [None] * 2
        
        # start GUI
        self.update()
     
        self.window.mainloop()
    
    # updating labels in GUI
    def update_text(self, data):
        for elem in data:
            #print('Hallo')
            if elem == None:
                return 
        self.steer_in.config(text="%2.3f" % data[0])
        self.accel_in.config(text="%2.3f" % data[1])
        self.brake_in.config(text="%2.3f" % data[2])

    # get video image and show them in GUI
    def update(self):
        # Get a frame from the video source
        ret, f = self.vid.get_frame()
        if ret:
            # split big image and convert them
            self.photo[0] = ImageTk.PhotoImage(image = Image.fromarray(cv2.resize(f[:,:],(w,h))))
            self.photo[1] = ImageTk.PhotoImage(image = Image.fromarray(cv2.resize(f[:,960*6:960*7],(w_r,h_r)))) # take last section for the rear view camera and resize it.
        
            for i in range(number_of_cameras):
                self.canvas[i].create_image(0, 0, image = self.photo[i], anchor = tkinter.NW)
        
        # get data from control
        data  = get_data_for_gui()
        #print(data)
        self.update_text(data)
        
        # run function again in certain amount of time
        self.window.after(self.delay, self.update)
 

# Videocapture class
# gives GUI frames from Gstreamer Pipeline
class MyVideoCapture:
    def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source ,cv2.CAP_GSTREAMER)
         if not self.vid.isOpened():
             #raise ValueError("Unable to open video source", video_source)
             print("ERROR: Videocapture not opened")
 
         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)        

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            #length = len(frame)
            #print(length)
            if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else: 
            return (False, None)
    
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
  
# start GUI    
def receive_video_from_car():    
     # Create a window and pass it to the Application object
     App(tkinter.Tk(), "Teleoperated Driving")
 
App(tkinter.Tk(), "Teleoperated Driving")