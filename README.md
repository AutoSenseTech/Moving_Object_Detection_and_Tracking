# Moving Object Detection and Tracking
Moving object detection and tracking is an evolving research field. Due to real-time object in dynamic tracking environment and different variety parameters input, it is huge topic. In this project, we aim to develop real-time object detection and tracking algorithm which combine optical flow and motion vector estimation for object detection and tracking in a sequence of frames.
## Software Preparation
```
ROS 
Opencv3 
CUDA 9.1 
ZED SDK 
Anaconda 
Ubuntu 16.04 or 14.04
```
### Install and Setup a Python Environment with Anaconda

1.Download and install Anaconda
In this step, we will download the Anaconda Python package for your platform.

Anaconda is a free and easy-to-use environment for scientific Python.


```
1. Visit the Anaconda homepage.
2. Click “Anaconda” from the menu and click “Download” to go to the download page.
```

2.Start and Update Anaconda

```
conda -V
python -V
conda update conda
conda update anaconda
```

## Hardware Preparation
### Sensors
```
Zed 2K Stereo Camera
```
### Autonomous Vehicle
```
Traxaas F1/10th Car Platform
```
### Board
```
NVIDIA Jetson TK1 developer kit
```
## Process
```
1. Embedding ROS System in Autonomous Vehicle
2. Getting a sequence of frame of moving object from sensors in dynamical environment.
3. The motion vector estimation techique aim to provide an estimation of object position from consecutive frames.
4. Giving the estimated position a control law based on the algorithm that was calculated make the autonomous vehicle follow the moving object.
```
## Authors

* **Weihan** - *Vanderbilt University Student* - [Weihan](https://github.com/wwtx9)

* **Feiyang** - *Vanderbilt University Phd Student* - [Feiyang](https://github.com/feiyangsb)

