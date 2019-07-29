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
import os


def dump_images(inbag, out_folder):

    bridge = CvBridge()

    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(2,2))


    output_folder = out_folder
    cam0_output_folder = os.path.join(output_folder, 'cam0', 'data')
    cam1_output_folder = os.path.join(output_folder,  'cam1', 'data')
    imu_folder = os.path.join(output_folder, 'imu0')

    if(not os.path.exists(cam0_output_folder)):
        os.makedirs(cam0_output_folder)
    if(not os.path.exists(cam1_output_folder)):
        os.makedirs(cam1_output_folder)
    if (not os.path.exists(imu_folder)):
        os.makedirs(imu_folder)

    asl_cam0 = os.path.join(output_folder, 'cam0', 'data.csv')
    dso_cam0 = os.path.join(output_folder, 'cam0', 'times.txt')
    asl_cam1 = os.path.join(output_folder, 'cam1', 'data.csv')
    dso_cam1 = os.path.join(output_folder, 'cam1', 'times.txt')

    asl_cam0 = open(asl_cam0, 'w+')
    dso_cam0 = open(dso_cam0, 'w+')
    asl_cam1 = open(asl_cam1, 'w+')
    dso_cam1 = open(dso_cam1, 'w+')

    orbslam_file0 =  os.path.join(output_folder, 'cam0', 'orb.txt')
    orbslam_file1 =  os.path.join(output_folder, 'cam1', 'orb.txt')
    orbslam_file0 = open(orbslam_file0, 'w+')
    orbslam_file1 = open(orbslam_file1, 'w+')

    imu_file = os.path.join(imu_folder, 'data.csv')
    imu_file = open(imu_file, 'w+')

    image_count = rosbag.Bag(inbag, 'r').get_message_count("/cam_fl/image_raw/compressed")
    # print(image_count)
    i=0

    for topic, msg, t in rosbag.Bag(inbag,'r').read_messages():
        if topic in ("/cam_fl/image_raw/compressed"):

            i=i+1

            np_arr = np.fromstring(msg.data, np.uint8)
            image_np = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

            stamp = msg.header.stamp
            asl_cam0.write('%s,%s\n' % (str(stamp), str(stamp)+'.png'))
            dso_cam0.write('%f\n' % (float(str(stamp))/1000000000))

            orbslam_file0.write('%s\n'% (str(msg.header.stamp)))
            enhanced_img = clahe.apply(image_np)

            cv2.imwrite(os.path.join(cam0_output_folder,str(stamp))+'.png', enhanced_img)

            percentage = int(float(i*100)/image_count)

            print (percentage, "% .. Completed")
        if topic in ("/cam_fr/image_raw/compressed"):

            np_arr = np.fromstring(msg.data, np.uint8)
            image_np = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

            stamp = msg.header.stamp
            asl_cam1.write('%s,%s\n' % (str(stamp), str(stamp)+'.png'))
            dso_cam1.write('%f\n' % (float(str(stamp))/1000000000))

            orbslam_file1.write('%s\n'% (str(msg.header.stamp)))
            enhanced_img = clahe.apply(image_np)


            cv2.imwrite(os.path.join(cam1_output_folder,str(stamp))+'.png', enhanced_img)

        if topic in ("/imu/imu"):
            w = msg.angular_velocity
            a = msg.linear_acceleration
            stamp = msg.header.stamp
            imu_file.write('%s,%f,%f,%f,%f,%f,%f\n' % (str(stamp), w.x, w.y, w.z, a.x, a.y, a.z))


    rospy.loginfo('Closing output bagfile and exit...')
    asl_cam0.close()
    dso_cam0.close()
    asl_cam1.close()
    dso_cam1.close()
    orbslam_file0.close()
    orbslam_file1.close()
    imu_file.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--inbag', help='input bagfile')
    parser.add_argument('--output_folder', help='output folder')

    args = parser.parse_args()

    inbag = args.inbag
    out_folder = args.output_folder
    dump_images(inbag, out_folder)
