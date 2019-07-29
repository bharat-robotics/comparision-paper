import cv2
import yaml
import numpy as np
import rosbag
import argparse
from cv_bridge import CvBridge
import glob
import os

def load_params():
    skip_lines = 0
    with open('/media/cokcybot/CA0EC88E0EC874CB/comparision_bag_files/TUM_VI/dataset-corridor2_512_16/dso/camchain.yaml') as infile:
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

def rectify_bag(input_folder, map1, map2, map3, map4):

    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(2, 2))

    # input_folder = '/home/cokcybot/tum_vi/dataset-room6_512_16/mav0'

    cam0_files = sorted(glob.glob(os.path.join(input_folder, 'cam0/data', '*.{}'.format('png'))))
    cam1_files = sorted(glob.glob(os.path.join(input_folder, 'cam1/data', '*.{}'.format('png'))))

    cam0_output_folder = os.path.join(input_folder, 'rectified', 'cam0', 'data')
    cam1_output_folder = os.path.join(input_folder, 'rectified', 'cam1', 'data')



    if(not os.path.exists(cam0_output_folder)):
        os.makedirs(cam0_output_folder)
    if(not os.path.exists(cam1_output_folder)):
        os.makedirs(cam1_output_folder)

    cam0_time = os.path.join(input_folder, 'rectified', 'cam0', 'times.txt')
    cam1_time = os.path.join(input_folder, 'rectified', 'cam1', 'times.txt')

    cam0_time_file = open(cam0_time, 'w+')
    cam1_time_file = open(cam1_time, 'w+')

    # print(cam0_files)
    for cam0_file in cam0_files:
        print('Undistorting', cam0_file)
        cv_image  = cv2.imread(cam0_file, cv2.IMREAD_GRAYSCALE)
        vals = cam0_file.split('/')
        val = vals[len(vals)-1]
        timestamp = val.split('.')[0]
        cam0_time_file.write('%s\n' % timestamp)
        undistorted_img = cv2.remap(cv_image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        enhanced_img = clahe.apply(undistorted_img)
        cv2.imwrite(os.path.join(cam0_output_folder, timestamp) + '.png', enhanced_img)

    for cam1_file in cam1_files:
        print('Undistorting', cam1_file)
        cv_image  = cv2.imread(cam1_file, cv2.IMREAD_GRAYSCALE)
        vals = cam1_file.split('/')
        val = vals[len(vals)-1]
        timestamp = val.split('.')[0]
        cam1_time_file.write('%s\n' % timestamp)
        undistorted_img = cv2.remap(cv_image, map3, map4, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        enhanced_img = clahe.apply(undistorted_img)
        cv2.imwrite(os.path.join(cam1_output_folder, timestamp) + '.png', enhanced_img)


    # bridge = CvBridge()


    # for topic, msg, t in rosbag.Bag(inbag,'r').read_messages():
    #     if topic in ("/cam0/image_raw", "/cam1/image_raw"):
    #
    #         cv_image = bridge.imgmsg_to_cv2(msg, "mono8")
    #         undistorted_img = cv2.remap(cv_image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    #
    #         cv2.imwrite(image_folder + str(msg.header.stamp)+'.png', undistorted_img)
    #         file.write('%s\n' % str(msg.header.stamp))
    #
    # file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Use Image Contrast enhancement to modify exposure changes '
                                                 'for Perceptin')
    parser.add_argument('--folder', help='input bagfile')
    args = parser.parse_args()

    map1, map2, map3, map4 = load_params()
    rectify_bag( args.folder, map1, map2, map3, map4)