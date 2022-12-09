Publisher_Nodes
======

The Source of inputs for the StreetDrone Vehicle Interface in ROS environment using Logitech Joystick. 


Features
------
1. Continuous software to Drive-by-Wireless (DBW) system handshake
2. Safety feature addes to avoid accident
3. Conversion maping of Input control data

Disclaimer
------
A trained safety driver must always be present in the vehicle in order to provide critical redundancy when operating the StreetDrone vehicles. 
Please follow the safety instructions provided in the documentation you received with your vehicles.

Requirements
------
##### - Ubuntu 20.04 LTS
##### - ROS Noetic [ros-noetic-desktop-full](http://wiki.ros.org/noetic/Installation/Ubuntu)
```
sudo apt install ros-noetic-desktop-full
```
##### - ROS Learning [ROS Tutorials](http://wiki.ros.org/ROS/Tutorials)
##### - Catkin Command Line Tools [catkin_tools](https://catkin-tools.readthedocs.io/en/latest/installing.html)
##### - Logitech Joystick-G29
Notes: To operate the Joystick install `pygame`
```
sudo apt install python3-pygame
```

Architecture
------
*sd_teleop_control:* This node is responsible for the main functionality of the package. Here the autonomous to manual mode handshake verification with the vehicle is implemented. 
The output of the `/twist_cmd` topic is used to publish the messages to the vehicle interface 

*aslan_msgs:* This message package is created for the control messages used in publisher nodes  




Building
------

1. Open a terminal and clone the entire repo with `git clone`. If you only want this package, go to the `/src` folder of your catkin workspace and copy the contents of only this package.

2. Build the package

for catkin make follow this commands:
Go to Workspace
```
$ source devel/setup.bash
$ catkin_make
```


Package Dependencies
------
Add below-mentioned dependencies, if required:
```
  <build_depend>geometry_msgs</build_depend>
  <build_export_depend>geometry_msgs</build_export_depend>
  <exec_depend>geometry_msgs</exec_depend>
  <build_depend>aslan_msgs</build_depend>
  <exec_depend>aslan_msgs</exec_depend>
  <exec_depend>sensor_msgs</exec_depend>
```    


Launch File Parameters
------
1. Open terminal and start ROS Master
```
$ roscore
```
2. Go to your Workspace and run the command
```
$ source devel/setup.bash
$ rosrun publisher_nodes sd_teleop_control
```
**Note**: `publisher_nodes` is package name.
          `sd_teleop_control` is file name.

To observe published messages, while Twizy is connected you can run below command:
```
$ source devel/setup.bash
$ roslaunch sd_vehicle_interface sd_vehicle_interface.launch sd_vehicle:=twizy <sd_gpts_imu:=peak sd_speed_source:=ndt_speed
```
If Twizy is not connected you can observe published messages via:
```
$ rostopic echo /twist_cmd
```
**Note**: `/twist_cmd` is topic name of published message


