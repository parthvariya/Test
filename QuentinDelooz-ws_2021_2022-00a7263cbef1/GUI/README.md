# Graphical User Interface #
Welcome to the description of the GUI. 

## What you can learn here? ##

* What is displayed in the GUI?
* How was it achieved?
* What do you have to do to run the code? (including prerequisites and step by step manual)
* What's up next?


## What is displayed in the GUI ##

The GUI is minimalistic due to unknown large lags with Tkinter (Tkinter is a GUI-Toolkit for python which was used by the last semester's project group).
Nevertheless it shows every necessary information to use the teleoperated driving function safely.

### The front view of the Twizy ###

The Twizy is equipped with all in all eight cameras.

* 3 cameras are showing the front view of the car -> Front-Left, Front-Center, Front-Right
* 2 cameras are showing the view to the left (one is facing a bit to the front and the other one a bit to the back) -> Left-Front, Left-Rear
* 2 cameras are showing the view to the right (one is facing a bit to the front and the other one a bit to the back) -> Right-Front, Right-Rear
* 1 camera is showing the rear view of the car -> Rear

In the GUI only three frames are displayed -> Left-Front, Front-Center, Right-Front
That's due to the capacity of the used free VPN. For the used values for the parameters (e.g. framerate, bitrate, framewidth, etc.) check out the "tx_video.py" file.
In the bottom center of the frame of the Front-Center camera there is the new ToD logo displayed. 

### The control information of the Twizy ###
In order to have the control data, from the control team, to be displayed in GUI-> use the file 'receive_data_for_gui'.
The data is mapped accroding to the requirement and for easy understanding of the controller(driver) who teleoperated drives twizzy.
Mapping is done within control file 'sd_teleop_control' under the defined funtion 'get_data_for_gui'.

## How it was achieved ##

### Video streaming ###

For the video streaming part at first a pipeline needs to be created (see "create_pipeline" function in "tx_video.py"). This pipeline is created using OpenCV.
OpenCV uses the help of Gstreamer to create and open the pipeline. With the used function it is possible to create a pipeline from the executing PC to a desired IP address incl. port.
We used the IP address of the receiving pc (ZODAC) of the free VPN. We used the UDP port with the number 19295 which is inoffically signed to "Google Talk Voice and Video connections" to transmit the video.



##  What do you have to do to run the code ##

### Prerequisites ###
To get the code to work there are some things you may have to install beforehand: Install the needed libraries!
Doing this, please be careful when installing **GStreamer**, **OpenCV** and **EasyPySpin**.

For the installation of GStreamer with OpenCV there is a corresponding HowTo in the HowTos folder.
Also: **DON'T** install EasyPySpin via pip. There is a library with the exact same name, but it has nothing to do with what we want to use here.
Click the following link where you can download the Spinnaker SDK **AND** the corresponding Python folder, which will give you needed instructions to install EasyPySpin.

--> https://flir.app.boxcn.net/v/SpinnakerSDK/folder/68522911814

All the other needed libraries can be easily installed via pip in the command line.

### How to run the code ##
 
1. Run the script called "tx_video.py" on the Twizy PC
2. Run the script called "receive_gui_with_cv.py" on the Receiving PC (We used the ZODAC PC)

### Troubleshooting ###
If something doesn't work, some quick ways to check:

* Check internet connection on both PCs, and make sure you're not in "campus" (firewall is blocking sending and receiving the video)
* Check if you get some gstreamer warnings. Even if they are "just" warnings: The pipeline might not be created because of this
* Check if the IP address used in the creation of the pipeline is correct (should be the address of the receiving PC)
* Check if the used port number in the creation of the pipeline is the same as in the receiving file

## Whats up next ##

* for final implementaion, 'receive_gui_with_cv' was used. However, further now tkinter should be used as it provides a large future scope for project development
* reduce delay in 'receive_gui_with_tkinter'
* Receive coloured Images from Twizy
* Including navigation (live location tracking)
* Get rid of "fisheye effect" 

### Further information on receiving the stream with Tkinter ###
1. Intialize tkinter
    tkinter.Tk()
2. Create the content and its respective grid for the GUI
3. creating a window
4. create the required number of canvas (here 2, one for 3 cameras all together [left,center,right] and other one for the rear view camera)
5. Divide canvas into a matrix format (8*24- each PC screen with 8*8 configuration)
    - In order to place the control data in required poition
    - Place the rear view camera canvas at the right grid position.
    (Future possibility:
        - Have left and right view camera in GUI
        - Have NAvigation system [MAP] in GUI)
6. Define the labels for the Data to be displayed 
7. end with the 'mainloop' to run the program.

### libraries, commands and their respective use ###

1. using cv2 :
    - Receive video
    - Receive adequate colour of the video (BGR2RGB)
    - Resize received frames

2. PIL
    - Extract section of frames from the streamed video
    - Creating Image and uploading in the respective Canvas.

3. Delay 
    defines the run the update command after certain amount of time (in ms)