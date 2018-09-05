#!python


import argparse

import rospy
from geometry_msgs.msg import PoseStamped
pose_topic = ''

class record_pose:
    def __init__(self, filename):
        rospy.init_node("tf_recorder")
        self.f = open(filename, "w")
        rospy.Subscriber(pose_topic, PoseStamped, self.pose_sub)
        rospy.spin()
        self.f.close()

    def pose_sub(self, pose_msg):
        position = pose_msg.pose.position
        quat = pose_msg.pose.orientation
        self.f.write('%s,%f,%f,%f,%f,%f,%f,%f\n' % (str(pose_msg.pose.header.stamp), position.x, position.y, position.z, quat.x, quat.y, quat.z, quat.w))

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Save memory and CPU usage")
    parser.add_argument('--file', help='file to record pose')
    args = parser.parse_args()
    filename = args.file

    record_pose(filename)

