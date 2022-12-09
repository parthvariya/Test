import tkinter
from sd_teleop_control import get_data_for_gui

class App:
    def __init__(self, window, window_title, video_source=0):
        # configure window
        self.window = window
        self.window.title(window_title)
        self.window.configure(bg='white')

        # configure GUI  
        self.data = tkinter.Frame(window, bg='white')
  
        # Create a canvas that can fit the above video source size
        self.data=tkinter.Canvas(window, bg = 'white', width=300, height=300)

        # give GUI a structure        
        self.data.grid(row=0,column=0,sticky='s')
        
        # defining labels
        self.accel = tkinter.Label(self.data, justify=tkinter.LEFT,padx=50, font="Verdana 15", text="Acceleration:", bg='white')
        self.brake = tkinter.Label(self.data, justify=tkinter.LEFT,padx=50,font="Verdana 15", text="Braking:", bg='white')
        self.steer = tkinter.Label(self.data, justify=tkinter.LEFT, pady=20,font="Verdana 15", text="Steering Angle:", anchor=tkinter.E, bg='white')
        self.accel_in = tkinter.Label(self.data, justify=tkinter.LEFT,padx=50,font="Verdana 15", text="0.00", bg='white')
        self.steer_in = tkinter.Label(self.data, justify=tkinter.LEFT, padx=50,font="Verdana 15", text="0.00", bg='white')
        self.brake_in = tkinter.Label(self.data, justify=tkinter.LEFT, padx=50,font="Verdana 15", text="0.00", bg='white')

        # place labels on content frame
        self.accel.grid(row=0, column=0)
        self.steer.grid(row=1, column=0)
        self.accel_in.grid(row=0, column=1)
        self.steer_in.grid(row=1, column=1)
        self.brake.grid(row=2, column=0)
        self.brake_in.grid(row=2, column=1)
     
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        
        # start GUI
        self.receive_data_from_joystick()
     
        self.window.mainloop()
    
    # updating labels in GUI
    def update_text(self, data):
        for elem in data:
            if elem == None:
                return 
        self.steer_in.config(text="%2.3f" % data[0])
        self.accel_in.config(text="%2.3f" % data[1])
        self.brake_in.config(text="%2.3f" % data[2])

    # get data and show them in GUI
    def receive_data_from_joystick(self):
        data  = get_data_for_gui()
        self.update_text(data)
        
        # run function again in certain amount of time
        self.window.after(self.delay, self.receive_data_from_joystick)
 
def receive_data_from_car():    
     # Create a window and pass it to the Application object
     App(tkinter.Tk(), "Data from Joystick")