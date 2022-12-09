import EasyPySpin
import numpy as np
import cv2

framerate=16 # in frames/second
w,h=(1920,1050) # desired width and height of the frames
cam_nr = 3 # number of used cameras for streaming the video
frames = [None] * cam_nr # frames of each camera
offset = 20
udp_port = 19295 # used udp port to send video through pipeline
bitrate = 900 # maximum bitrate of created pipeline

#            rear L      rear C      rear R     front R     front C     front L
cam_ids = ["20513338", "20513343", "20513347", "20513349", "20513338", "20513341"] # contains serialnumbers of the cameras to access them

def stream():
    cap = EasyPySpin.MultipleVideoCapture(cam_ids[5], cam_ids[4], cam_ids[3])
    out_send = create_pipeline(framerate, cam_nr, w, h, udp_port, bitrate)

    if not all(cap.isOpened()):
        print("All cameras can't open\nPlease check the connection\nexit")

    # read logo
    img2 = cv2.imread('logo.jpg')
    img2 = cv2.resize(img2, (int(w/6), int(w/6*0.4)))
    # create values for ROI in frame to put logo on
    rows,cols,channels = img2.shape
    # create mask of logo and create its inverse mask also
    img2gray = cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # take only region of logo from logo image
    img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
    
    while True:
        read_values = cap.read()
        
        for i, (ret, frame) in enumerate(read_values):
            if not ret:
            # so that the code doesn't stop because of one empty frame -> when frame empty show black screen
                frame = np.zeros((h,w,3), dtype=np.uint8)
            else:
                frame = cv2.resize(frame, (w,h))
                frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)

            if i == 1:
                # create ROI in frame
                roi = frame[-(rows+offset):-offset, round((w/2)-cols/2):round((w/2)+cols/2)]
                # black-out the area of logo in ROI
                img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
                # put logo in ROI and modify the main image
                dst = cv2.add(img1_bg,img2_fg)
                frame[-(rows+offset):-offset, round((w/2)-cols/2):round((w/2)+cols/2)] = dst    
            frames[i] = frame

        # put frames together (side by side, horizontally)
        frame_con = cv2.hconcat(frames)
        out_send.write(frame_con)

    cap.release()
    out_send.release()
    cv2.destroyAllWindows()

def create_pipeline(framerate, cam_nr, width, height, port, bitrate, frame_is_colored=True):
    # function to create pipeline
    out_send = cv2.VideoWriter('appsrc is-live=true ! videoconvert ! x264enc tune=zerolatency noise-reduction=100000 byte-stream=true threads=8 key-int-max=15 bitrate=' + str(bitrate) + ' ! rtph264pay ! udpsink host=192.168.196.125 port=' + str(port),cv2.CAP_GSTREAMER,0, framerate, (width*cam_nr,height), frame_is_colored)
    return out_send

def main():
    stream()
    
if __name__ == "__main__":
    main()