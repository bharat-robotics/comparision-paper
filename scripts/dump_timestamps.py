#!/usr/bin/python

import rospy
from sensor_msgs.msg import Imu
import argparse

class dump_stamps:
    def __init__(self, filename):
        rospy.init_node("tf_recorder")
        self.f = open(filename, "w")
        rospy.Subscriber('/pirvs/imu', Imu, self.imu_sub)
        rospy.spin()
        self.f.close()

    def imu_sub(self, imu_msg):
        acc = imu_msg.linear_acceleration
        ang_vel = imu_msg.angular_velocity
        self.f.write('%f,%f,%f,%f,%f,%f,%f\n' % (imu_msg.header.stamp.to_sec(), acc.x, acc.y, acc.z, ang_vel.x, ang_vel.y, ang_vel.z))



if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Save memory and CPU usage")
    parser.add_argument('--file', help='file to record pose')
    args = parser.parse_args()
    filename = args.file

    dump_stamps(filename)