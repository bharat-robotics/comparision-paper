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


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def enhance_images(inbag, outbag):
    rospy.loginfo(' Processing input bagfile: %s', inbag)
    rospy.loginfo(' Writing to output bagfile: %s', outbag)

    print(inbag)
    outbag = rosbag.Bag(outbag, 'w')
    original_stamp = open('original-stamp.txt', 'w')
    sync_stamp = open('synced_stamp.txt', 'w')
    less_stamp = open('less_stamp.txt', 'w')

    bridge = CvBridge()

    less_stamps = []
    more_stamps = []
    msgs = []
    cam_info_msg = []

    for topic, msg, t in rosbag.Bag(inbag,'r').read_messages():
        if topic in ("/cam_fr/image_raw/compressed"):
            more_stamps.append(msg.header.stamp.to_sec())
            msgs.append(msg)
            original_stamp.write('%f\n'% msg.header.stamp.to_sec() )
        elif topic in ("/cam_fl/image_raw/compressed"):
            less_stamps.append(round(msg.header.stamp.to_sec(),4))
        elif topic in ("/cam_fr/image_raw/cam_info"):
            cam_info_msg.append(msg)

    # print(len(more_stamps))
    # print(len(less_stamps))

    # synced_stamp = []
    # for stamp in less_stamps:
    #     closest = find_nearest(np.array(more_stamps), stamp)
    #     synced_stamp.append(closest)
    #     sync_stamp.write('%f\n' % closest)
    #
    # #
    # print(len(synced_stamp))
    for topic, msg, t in rosbag.Bag(inbag, 'r').read_messages():
        if topic in ("/cam_fl/image_raw/compressed"):
            index = find_nearest(np.array(more_stamps), msg.header.stamp.to_sec())
            sync_message = msgs[index]
            sync_message.header.stamp =  msg.header.stamp
            outbag.write("/cam_fr/image_raw/compressed", sync_message, msg.header.stamp)
        if topic in ("/cam_fl/image_raw/cam_info"):
            index = find_nearest(np.array(more_stamps), msg.header.stamp.to_sec())
            sync_message = cam_info_msg[index]
            sync_message.header.stamp = msg.header.stamp
            outbag.write("/cam_fr/image_raw/cam_info", sync_message, msg.header.stamp)

    for topic, msg, t in rosbag.Bag(inbag, 'r').read_messages():
        if topic not in ("/cam_fr/image_raw/compressed", "/cam_fr/image_raw/cam_info"):
            outbag.write(topic, msg, msg.header.stamp)

    rospy.loginfo('Closing output bagfile and exit...')
    outbag.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Use Image Contrast enhancement to modify exposure changes '
                                                 'for Perceptin')
    parser.add_argument('--inbag', help='input bagfile')
    parser.add_argument('--outbag', help='output bagfile', default='test.bag')
    args = parser.parse_args()

    try:
        enhance_images(args.inbag,args.outbag)
    except (Exception):
        import traceback
        traceback.print_exc()