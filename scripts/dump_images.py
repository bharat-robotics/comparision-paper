#!/usr/bin/python

import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import argparse
import cv2
import os
import numpy as np

folder = '/home/cokcybot/husky_indoor_mav'
left_folder = folder + '/left/cam0'
right_folder = folder + '/right/'
filename = folder + '/times.txt'

class dump_stamps:
    def __init__(self):
        if (not os.path.exists(left_folder)):
            os.makedirs(left_folder)
        if (not os.path.exists(right_folder)):
            os.makedirs(right_folder)
        rospy.init_node("tf_recorder")
        self.f = open(filename, "w")
        rospy.Subscriber('/pirvs/left/image_raw/compressed', CompressedImage, self.left_image_sub)
        rospy.Subscriber('/pirvs/right/image_raw/compressed', CompressedImage, self.right_image_sub)
        self.bridge = CvBridge()


        rospy.spin()
        self.f.close()

    def left_image_sub(self, img_msg):
        np_arr = np.fromstring(img_msg.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(left_folder+str(img_msg.header.stamp)+'.png', image_np)
        self.f.write('%s\n' % str(img_msg.header.stamp))

    def right_image_sub(self, img_msg):
        np_arr = np.fromstring(img_msg.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(right_folder+str(img_msg.header.stamp)+'.png', image_np)



if __name__=='__main__':

    # parser = argparse.ArgumentParser(description='Use Image Contrast enhancement to modify exposure changes '
    #                                             'for Perceptin')
    # parser.add_argument('--folder', help='input bagfile')
    # args = parser.parse_args()

    file = dump_stamps()