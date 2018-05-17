#!/usr/bin/python

# this file change the imu data from perceptin to accomodate
# accelerometer and gyroscope bias

from __future__ import print_function

import rospy
import cv2
from sensor_msgs.msg import CompressedImage
import numpy as np

import message_filters


class enhance_image:

    def __init__(self):

        self.left_subscriber = message_filters.Subscriber("/pirvs/left/image_raw/compressed",CompressedImage, queue_size = 1)
        self.right_subscriber = message_filters.Subscriber("/pirvs/right/image_raw/compressed",CompressedImage, queue_size = 1)

        self.left_image_pub = rospy.Publisher("/pirvs/left/image/compressed",CompressedImage,queue_size=5)
        self.right_image_pub = rospy.Publisher("/pirvs/right/image/compressed",CompressedImage,queue_size=5)

        self.histenhance = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))

        self.time_sync = message_filters.ApproximateTimeSynchronizer([self.left_subscriber,self.right_subscriber], 10, 0.1)

        self.time_sync.registerCallback(self.img_callback)

    def img_callback(self,left_msg,right_msg):

        ##Decoding image ##
        left_np_arr = np.fromstring(left_msg.data, np.uint8)
        left_image_np = cv2.imdecode(left_np_arr, cv2.IMREAD_GRAYSCALE)
        right_np_arr = np.fromstring(right_msg.data, np.uint8)
        right_image_np = cv2.imdecode(right_np_arr, cv2.IMREAD_GRAYSCALE)


        ##Contrast Enhancement ##
        left_enhanced_img = self.histenhance.apply(left_image_np)
        right_enhanced_img = self.histenhance.apply(right_image_np)


        #### Create CompressedIamge ####
        enhanced_left_msg = CompressedImage()
        enhanced_left_msg.header.stamp = left_msg.header.stamp
        enhanced_left_msg.format = "jpeg"
        enhanced_left_msg.data = np.array(cv2.imencode('.jpg', left_enhanced_img)[1]).tostring()

        enhanced_right_msg = CompressedImage()
        enhanced_right_msg.header.stamp = right_msg.header.stamp
        enhanced_right_msg.format = "jpeg"
        enhanced_right_msg.data = np.array(cv2.imencode('.jpg', right_enhanced_img)[1]).tostring()

        # Publish new image
        self.left_image_pub.publish(enhanced_left_msg)
        self.right_image_pub.publish(enhanced_right_msg)


if __name__ == "__main__":
    image_enhance = enhance_image()
    rospy.init_node('enhance_images', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down ROS Image Enhancement module")
    cv2.destroyAllWindows()