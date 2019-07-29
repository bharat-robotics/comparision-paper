#!/usr/bin/python

#this file change the imu data from perceptin to accomodate
#accelerometer and gyroscope bias

from __future__ import print_function


import rosbag
import rospy
import argparse

topics = ["/pirvs/left/image_raw/compressed","/pirvs/right/image_raw/compressed","/axis/image_raw/compressed",
          "/gps/fix","/gps/nmea_sentence","/gps/time_reference","/gps/vel","/imu/data","/imu/data_raw",
          "/imu/magnetic_field","/imu_um6/data","/odometry/filtered","/odometry/gps","/pirvs/imu","/pirvs/imu/raw",
          "/scan","/tf"]

def filter_topics(inbag,outbag):
    rospy.loginfo(' Processing input bagfile: %s', inbag)
    rospy.loginfo(' Writing to output bagfile: %s', outbag)

    outbag = rosbag.Bag(outbag,'w',allow_unindexed='true')

    for topic, msg, t in rosbag.Bag(inbag,'r').read_messages():
        if topic in topics:
            outbag.write(topic,msg,t)

    rospy.loginfo('Closing output bagfile and exit...')
    outbag.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Use Image Contrast enhancement to modify exposure changes '
                                                 'for Perceptin')
    parser.add_argument('--inbag',help='input bagfile')
    parser.add_argument('--outbag',help='output bagfile')
    args = parser.parse_args()

    try:
        filter_topics(args.inbag,args.outbag)
    except (Exception):
        import traceback
        traceback.print_exc()