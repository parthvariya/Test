# Communication #

## What you can learn here? ##

-->How to create a VPN network.


1) There are many vpn providers. For the semester project we had made use zerotier to build and setup the network. Here is the link for the zerotier website : https://www.zerotier.com/

2) Start building the network by signing with google account or create a one as you prefer

3) Once the network is built, You will be provided with a network ID and this is like a network cloud address.

4) Note down the network ID 

5) Install zerotier on your Linux machine or windows machine. Lines of codes are available in the webpage of zerotier for Linux machine. For windows machine you will have download a .exe file and install it in the machine
Linux codes

curl -s https://install.zerotier.com | sudo bash

6) Use the network ID to join the network either in your linux or windows machine

Linux machine : sudo zerotier -cli join “your network ID” 
Replace the your network ID with the ID number  and remove “ ” which look like this 17d709436cba3435

7) Your device is now added to the network of zerotier. 

8) Zerotier will assign a new network adapter to your machine 

9) If you do an IPconfig you will see something like Ethernet adapter zerotier One [ your network ID]



Network performance monitoring


1) You can use network performance tools like iperf3 or netperf to evaluate the vpn network that was established.

2) Performance of the network was outputted into JSON format, where network performance value will be outputted to python readable tuple format.

3) Iperf3 –c 192.168….. –J –B 20 –u >filename.txt and iperf3 –s  (source)

4) There are many options in the iperf3 tools. Download the iper3.exe file and use command window to display the options of the iperf3 tool. Type iperf3 to get the options.

5) Out put format of the json sample file is uploaded to bitbucket repository.



6) If you want to analyse the network performance then you can use the this json file and use the plotting python code provided in the bitbucket to plot the performance curve.





Communication between twizzy and remote desktop/controller.


1) ROS master and slave concept was used to setup the communication of control message between the twizzy and remote pc.

2) Add these into .bashrc file for both twizzy  and remote pc.

3) Twizzy is the receiver node and remote pc is the publisher nodes.

4) Reciever

export ROS_MASTER_URI=http://localhost:11311/

export ROS_HOSTNAME=”your pc VPN IP of this machine”

export ROS_IP=”Your pc VPN IP of this machine”


5) Publisher

export ROS_MASTER_URI=http://”receiver vpn IP”:11311/

export ROS_HOSTNAME=”your pc VPN IP of this machine”

export ROS_IP=”Your pc VPN IP of this machine”



Communication between cameras from twizzy to remote desktop.

1) Gstreamer pipelines used for streaming has the fields to specify the hostname ip where you can specify the ip address of the remote desktop PC which is reciver  here.


Sender pipeline


cv2.VideoWriter('appsrc ! decodebin ! videoconvert ! x264enc tune=zerolatency bitrate=10000 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.0.3 port=5000',cv2.CAP_GSTREAMER,0, frames, (w,h), True)


