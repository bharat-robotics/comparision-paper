#!python


import sys

import rospy
import argparse
from tf import TransformListener, transformations
from tf2_msgs.msg import TFMessage


class myNode:
    def __init__(self, filename):
        rospy.init_node("tf_recorder")
        self.map_frame = 'map'
        self.robot_frame = 'rebvo_frame_cam'
        self.f = open(filename, "w")
        self.tf = TransformListener()
        rospy.Subscriber("/tf", TFMessage, self.record_tf)
        rospy.spin()
        self.f.close()
        print("Stream closed")

    def record_tf(self, msg):
        for t in msg.transforms:
            if (t.header.frame_id == self.map_frame and t.child_frame_id == self.robot_frame):
                m = t.transform.translation
                q = t.transform.rotation
                rpy = transformations.euler_from_quaternion((q.x, q.y, q.z, q.w))
                self.f.write("%f,%f,%f,%f,%f,%f,%f,%f\n" % (t.header.stamp.to_sec(), m.x, m.y, m.z, q.x, q.y, q.z, q.w))


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Record TF")
    parser.add_argument('--file', help='file to record pose')
    args = parser.parse_args()
    filename = args.file

    node = myNode(filename)
    print("Done")
