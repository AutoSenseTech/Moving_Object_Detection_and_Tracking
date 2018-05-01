#!/usr/bin/env python

import rospy
from move_target_track.msg import trackPara

def callback(data):
    print data.length
    rospy.loginfo("length = %d, radius = %d" % (data.length, data.radius))

def listener():
    rospy.init_node('custom_listener', anonymous=True)
    rospy.Subscriber("tracker", trackPara, callback)

    rospy.spin()
if __name__ == '__main__':
    listener()
