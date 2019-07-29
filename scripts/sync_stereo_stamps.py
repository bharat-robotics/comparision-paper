#!/usr/bin/python

#this file change the imu data from perceptin to accomodate
#accelerometer and gyroscope bias

from __future__ import print_function


import rosbag
import rospy
import argparse
import cv2
from cv_bridge import CvBridge
import numpy as np

def enhance_images(inbag, outbag):
    rospy.loginfo(' Processing input bagfile: %s', inbag)
    rospy.loginfo(' Writing to output bagfile: %s', outbag)

    print(inbag)
    outbag = rosbag.Bag(outbag, 'w')

    stamps = []
    for topic, msg, t in rosbag.Bag(inbag,'r').read_messages():
        if topic in ('/slave1/image_raw/compressed'):
            stamps.append(msg.header.stamp)

    i = 0
    for topic, msg, t in rosbag.Bag(inbag, 'r').read_messages():
        if topic in ('/slave2/image_raw/compressed'):
            outbag.write(topic, msg, stamps[i])
            i = i + 1
            print(i)
        else:
            outbag.write(topic, msg, msg.header.stamp)

    rospy.loginfo('Closing output bagfile and exit...')
    outbag.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Use Image Contrast enhancement to modify exposure changes '
                                                 'for Perceptin')
    parser.add_argument('--inbag',help='input bagfile')
    parser.add_argument('--outbag',help='output bagfile')
    args = parser.parse_args()

    try:
        enhance_images(args.inbag,args.outbag)
    except (Exception):
        import traceback
        traceback.print_exc()