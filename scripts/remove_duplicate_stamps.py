#!/usr/bin/python

#this file change the imu data from perceptin to accomodate
#accelerometer and gyroscope bias

from __future__ import print_function


import rosbag
import rospy

def enhance_images(inbag,outbag):
   rospy.loginfo(' Processing input bagfile: %s', inbag)
   rospy.loginfo(' Writing to output bagfile: %s', outbag)

   outbag = rosbag.Bag(outbag,'w',allow_unindexed='true')

   previous_stamp = 0

   for topic, msg, t in rosbag.Bag(inbag,'r').read_messages():
       if topic in ("/pirvs/imu"):
           if(previous_stamp!=msg.header.stamp):
               outbag.write(topic,msg,t)
               previous_stamp = msg.header.stamp
       else:
           outbag.write(topic, msg, t)

   rospy.loginfo('Closing output bagfile and exit...')
   outbag.close()

if __name__=="__main__":

   inbag = '/home/cokcybot/husky_outdoor_bushes.bag'
   outbag = '/home/cokcybot/husky_outdoor.bag'
   try:
       enhance_images(inbag,outbag)
   except (Exception):
       import traceback
       traceback.print_exc()