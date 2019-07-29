#!/usr/bin/python

from __future__ import print_function


def sync_stamps():
    infile = '/home/cokcybot/Downloads/gt-husky-outdoor.csv'
    outfile = '/home/cokcybot/Comparision-Paper/gt-husky-outdoor-sync.txt'
    # offset = 1527114914.1527114914 - 1527113168.336255264
    offset =   1527114499.197999954 - 1527112752.754836283
    input_gt = open(infile, 'r')
    sync_gt = open(outfile, 'w+')

    lines = input_gt.readlines()
    for line in lines:
        line = line.split(',')
        line = [float(x) for x in line]
        stamp = line[0] + offset
        sync_gt.write('%f,%f,%f,%f\n' % (stamp, line[1], line[2], line[3]))


    input_gt.close()
    sync_gt.close()

if __name__=="__main__":
    sync_stamps()