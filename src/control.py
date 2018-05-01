#!/usr/bin/env python

import rospy
import sys
from move_target_track.msg import drive_param
from move_target_track.msg import pid_input

##use to turn the steering of the car to the center position if any 
# mechanical misalignment
servo_offset = 7.0 

# previous error, variable used in PID equation
prev_error = 0.0 

# Proportional constant for PID equation
kp = rospy.get_param("kp", 14.0)

# Differential constant for PID equation
kd = rospy.get_param("kd", 0.09)

# amount to scale error by
scale = rospy.get_param("scale", 0.25)

# drive_param message publisher
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

#subscriber boolean
sub_bool = 0

##check_bounds
##checks to see if the error is within the given bounds of (-100,100)
def check_bounds(error):
	low = -100
	high = 100
	return error >= low and error <= high

def trim_angle(angle):
	if angle > 100:
		angle = 100
	if angle < -100:
		angle = -100
	return angle

def control(data):
    global servo_offset
    global prev_error
    global kp
    global kd
    global scale
    global pub
    global sub_bool
    
    sub_bool = 1
	## Your code goes here
	# 1. Scale the error (amplify error by some suitable value)
	# 2. Apply the PID equation on error (consider servo_offset)
	# 3. Make sure the error is within bounds of (-100, 100)
 	
	## Error is scaled to reflect proper angle value
	# 7 seems to be a good scale
    error = data.pid_error * scale

	##PID EQ
	# Angle value is sent to talker and converted to PWM signal
	# 100 corresponds to max turn to right; -100 is left
    angle = kp*error + kd*(error - prev_error) + servo_offset
    prev_error = error

    angle = trim_angle(angle)
	##make sure in bounds, otherwise raise error
    if check_bounds(angle):
        msg = drive_param();
        msg.velocity = data.pid_vel	
        msg.angle = angle
        msg.error = error
        pub.publish(msg) #which then goes to talker.py -> converter.py
    else:
        print 'error angle %4.2f not in given bounds' % angle
        raise ValueError('error not in given bounds')

if __name__ == '__main__':
	global sub_bool
	print("Listening to error for PID")
	raw_input("Press enter to drive...")
	rospy.init_node('control', anonymous=True)
	rospy.Subscriber("error", pid_input, control) #gets from distance finder
	if sub_bool == 0:
		msg = drive_param()
		msg.velocity = 0.0
		msg.angle = 0.0
		msg.error = 0.0
		pub.publish(msg)
	rospy.spin()
	
