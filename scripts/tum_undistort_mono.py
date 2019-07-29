#!/usr/bin/python

#this file change the imu data from perceptin to accomodate
#accelerometer and gyroscope bias

from __future__ import print_function


import rosbag
import rospy
import argparse
import cv2
from cv_bridge import CvBridgeError, CvBridge
import numpy as np
import yaml

def load_params():
    skip_lines = 0
    with open('//home/cokcybot/tum_vi/camchain-imucam-imucalib.yaml') as infile:
        for i in range(skip_lines):
            _ = infile.readline()
        data = yaml.load(infile)

    # You should replace these 3 lines with the output in calibration step
    DIM = (512, 512)
    # K=np.array(YYY)
    # D=np.array(ZZZ)

    [fu, fv, pu, pv] = data['cam0']['intrinsics']
    # https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0
    K = np.asarray([[fu, 0, pu], [0, fv, pv], [0, 0, 1]])  # K(3,3)
    D = np.asarray(data['cam0']['distortion_coeffs'])  # D(4,1)

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)

    [fu, fv, pu, pv] = data['cam1']['intrinsics']
    # https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0
    K = np.asarray([[fu, 0, pu], [0, fv, pv], [0, 0, 1]])  # K(3,3)
    D = np.asarray(data['cam1']['distortion_coeffs'])  # D(4,1)

    map3, map4 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)


    return  map1, map2, map3, map4

def undistort(inbag,outbag, map1, map2, map3, map4):
    rospy.loginfo(' Processing input bagfile: %s', inbag)
    rospy.loginfo(' Writing to output bagfile: %s', outbag)

    outbag = rosbag.Bag(outbag, 'w')
    bridge = CvBridge()

    for topic, msg, t in rosbag.Bag(inbag,'r').read_messages():
        if topic in ("/cam0/image_raw"):

            cv_image = bridge.imgmsg_to_cv2(msg, 'mono8')
            undistorted_img = cv2.remap(cv_image, map1, map2, interpolation=cv2.INTER_LINEAR,
                                        borderMode=cv2.BORDER_CONSTANT)
            image_msg = bridge.cv2_to_imgmsg(undistorted_img, 'mono8')
            image_msg.header.stamp = msg.header.stamp
            outbag.write(topic, image_msg, msg.header.stamp)

        elif topic not in ("/cam1/image_raw"):
            outbag.write(topic, msg, msg.header.stamp)

    rospy.loginfo('Closing output bagfile and exit...')
    outbag.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Use Image Contrast enhancement to modify exposure changes '
                                                 'for Perceptin')
    parser.add_argument('--inbag',help='input bagfile')
    parser.add_argument('--outbag',help='output bagfile')
    args = parser.parse_args()

    map1, map2, map3, map4 = load_params()
    try:
        undistort(args.inbag,args.outbag, map1, map2, map3, map4)
    except (Exception):
        import traceback
        traceback.print_exc()