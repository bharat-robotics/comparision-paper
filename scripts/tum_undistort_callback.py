import cv2
import argparse
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import os
import rospy



cam0_topic = '/cam0/image_rectified'
cam1_topic = '/cam1/image_rectified'

class save_undistort:
    def __init__(self, input_folder):
        self.cam0_output_folder = os.path.join(input_folder, 'rectified_undistort', 'cam0', 'data')
        self.cam1_output_folder = os.path.join(input_folder, 'rectified_undistort', 'cam1', 'data')

        if (not os.path.exists(self.cam0_output_folder)):
            os.makedirs(self.cam0_output_folder)
        if (not os.path.exists(self.cam1_output_folder)):
            os.makedirs(self.cam1_output_folder)

        self.cam0_time = os.path.join(input_folder, 'rectified_undistort', 'cam0', 'times.txt')
        self.cam1_time = os.path.join(input_folder, 'rectified_undistort', 'cam1', 'times.txt')

        self.cam0_time_file = open(self.cam0_time, 'w+')
        self.cam1_time_file = open(self.cam1_time, 'w+')

        rospy.init_node("save_images")

        rospy.Subscriber(cam0_topic, Image, self.first_image_callback)
        rospy.Subscriber(cam1_topic, Image, self.first_image_callback)

        self.bridge = CvBridge()
        rospy.spin()

        self.cam0_time_file.close()
        self.cam1_time_file.close()

    def first_image_callback(self, img_msg):
        cv_image = self.bridge.imgmsg_to_cv2(img_msg)
        timestamp = str(img_msg.header.stamp)
        self.cam0_time_file.write('%s\n' % timestamp)
        print('Undistorting', timestamp, '.png')
        cv2.imwrite(os.path.join(self.cam0_output_folder, timestamp) + '.png', cv_image)

    def second_image_callback(self, img_msg):
        cv_image = self.bridge.imgmsg_to_cv2(img_msg)
        timestamp = str(img_msg.header.stamp)
        self.cam1_time_file.write('%s\n' % timestamp)
        print('Undistorting', timestamp, '.png')
        cv2.imwrite(os.path.join(self.cam1_output_folder, timestamp) + '.png', cv_image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Use Image Contrast enhancement to modify exposure changes '
                                                 'for Perceptin')
    parser.add_argument('--folder', help='input bagfile')
    args = parser.parse_args()

    save_undistort(args.folder)
    # map1, map2 = load_params()
    # rectify_bag( args.folder, map1, map2)