#!python

import argparse

pose_topic = '/lsd_slam/pose'
frame_file = '/home/cokcybot/ros_workspaces/lsd_ws/lsd_pose.txt'
stamps_file = '/home/cokcybot/Downloads/EuroC/MH_03_copy/cam0/times.txt'
pose_file = '/home/cokcybot/ros_workspaces/catkin_ws/src/comparision-paper/scripts/lsd_mh_03.txt'

def sync_stamps(filename):

    file  = open(filename, 'w+')

    stamps = []
    with open(stamps_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            stamps.append(float(line[1]))

    frames = []

    with open(frame_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            line = [float(x) for x in line]
            frames.append(int[line[0]])
            file.write('%f,%f,%f,%f,%f,%f,%f,%f\n' % (stamps[int[line[0]]], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))

    # print len(stamps)
    # print len(frames)


    # with open(pose_file) as f:
    #     lines = f.readlines()
    #     for i, line in enumerate(lines):
    #         line = line.split(',')
    #         line = [float(x) for x in line]
    #         file.write('%f,%f,%f,%f,%f,%f,%f,%f\n' % (stamps[frames[i]], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))

    file.close()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Save sync file")
    parser.add_argument('--file', help='file to record pose')
    args = parser.parse_args()
    filename = args.file
    sync_stamps(filename)
