#!/usr/bin/env python

import rospy
from move_target_track.msg import drive_param
from move_target_track.msg import drive_values
from std_msgs.msg import Bool
from std_msgs.msg import Int16

#This is the subscriber node

given_vel = 0
given_ang = 0
stop_bool = 0
pub = rospy.Publisher('drive_pwm', drive_values, queue_size=10)
stop_pub = rospy.Publisher('eStop', Bool, queue_size=10)

#callback function that listens to the drive_parameters topic
#logs info from drive_param msg
#calls talker() to send data to teensy
#need to map the incoming values to the needed PWM values
#stored in custom messages ("drive_values") and published via "drive_pwm" topic
def callback(data): 
	if stop_bool == 0:
		print'velocity=%s angle=%s' % (data.velocity, data.angle)
		given_vel = data.velocity
		given_ang = data.angle
		pwm_vel = mapValue(given_vel, -100,100,6554,13108)
		pwm_ang = mapValue(given_ang, -100,100,6554,13108)
		msg = drive_values()
		msg.pwm_drive = pwm_vel
		msg.pwm_angle = pwm_ang
		pub.publish(msg)

def flagCallback(msg):
	global stop_bool
	if msg.data == 1:
		pwm_vel = mapValue(0, -100, 100, 6554, 13108)
		pwm_ang = mapValue(0, -100, 100, 6554, 13108)
		new_msg = drive_values()
		new_msg.pwm_drive = pwm_vel
		new_msg.pwm_angle = pwm_ang
		pub.publish(new_msg)
		stop_bool = 1 

#Subscriber to the drive_parameters topic
def talker():
	rospy.init_node('talker',anonymous=True)
	stop_pub.publish(False)
	rospy.Subscriber('drive_parameters', drive_param, callback)
	rospy.Subscriber('path_stop', Int16, flagCallback)
	#doesn't exit until node is stopped	
	rospy.spin() 
	

#Maps the given keyboard value to that of a pwm value 
#raises an error if the value is not in range
##******ESC
## Forward at +8 ********
## Backwards at -10 *******
def mapValue(value, key_min, key_max, pwm_min, pwm_max):
	if(not(value > key_max or value < key_min)):
		key_span = key_max - key_min
		pwm_span = pwm_max - pwm_min
		val_scale = (float(pwm_span)/key_span)
		
		return (value - key_min)*val_scale + pwm_min
	raise ValueError('The given value was not in range (-100, 100)')


if __name__ == '__main__':
	print("talker started")
	talker()


