#!/usr/bin/python

import argparse

def write_timestamps(infile, outfile):

    outputfile = open(outfile, 'w')

    with open(infile,'r') as read_file:
        lines = read_file.readlines()
        i = 0
        for line in lines:
            line = line.split(',')
            outputfile.write('%d  %f\n' % (i, (float(line[0])/1000000000)))
            i = i+1

    outputfile.close()



if __name__=='__main__':
    parser = argparse.ArgumentParser(description="dumps timestamps from euroc to tum format")
    # parser.add_argument('--p', metavar='N', type=int, nargs='+', help='list of processes')
    parser.add_argument('--infile', help='input file from euroc')
    parser.add_argument('--opfile', help='timestamp file')

    args = parser.parse_args()
    write_timestamps(args.infile, args.opfile)