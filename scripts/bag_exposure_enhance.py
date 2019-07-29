#!/usr/bin/python

#this file change the imu data from perceptin to accomodate
#accelerometer and gyroscope bias

from __future__ import print_function


import rosbag
import rospy
import argparse
import cv2
from cv_bridge import CvBridgeError
import numpy as np

def enhance_images(inbag,outbag):
    rospy.loginfo(' Processing input bagfile: %s', inbag)
    rospy.loginfo(' Writing to output bagfile: %s', outbag)

    print(inbag)
    outbag = rosbag.Bag(outbag,'w',allow_unindexed='true')
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5, 5))

    for topic, msg, t in rosbag.Bag(inbag,'r').read_messages():
        if topic in ("/pirvs/left/image_raw/compressed","/pirvs/right/image_raw/compressed"):
            try:
                #### direct conversion to CV2 ####
                np_arr = np.fromstring(msg.data, np.uint8)
                image_np = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
            except CvBridgeError as e:
                print(e)
            enhanced_img = clahe.apply(image_np)
            #
            # cv2.imshow('Enhanced Image',enhanced_img)
            # cv2.waitKey(1)

            msg.data = np.array(cv2.imencode('.jpg', enhanced_img)[1]).tostring()
            outbag.write(topic,msg,t)
        else:
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
        enhance_images(args.inbag,args.outbag)
    except (Exception):
        import traceback
        traceback.print_exc()