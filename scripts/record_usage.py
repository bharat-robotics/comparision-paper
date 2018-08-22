#!/usr/bin/python

import argparse
import subprocess
import atexit
import time

def closefiles(cpufile, memfile):
    cpufile.close()
    memfile.close()

if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Save memory and CPU usage")
    parser.add_argument('--p', metavar='N', type=int, nargs='+', help='list of processes')
    parser.add_argument('--mem_file', help='file to reocrd memory usage')
    parser.add_argument('--cpu_file', help='file to record CPU usage')
    args = parser.parse_args()
    process = args.p

    # print(args.cpu_file)
    # print(args.mem_file)
    # print(args.p)
    cpu_file = open(args.cpu_file, 'w+')
    mem_file = open(args.mem_file, 'w+')

    atexit.register(closefiles, cpu_file, mem_file)

    while True:
        total_memory = 0
        total_cpu = 0
        for p in process:
            # print('Finding memory usage for pid:', p)
            try:
                output = subprocess.check_output(['ps', '-p', str(p), '-o', '%cpu,%mem'])
                for line in output.splitlines():
                    if '%' not in line:
                        total_cpu += float(line.split()[0])
                        total_memory += float(line.split()[1])
            except subprocess.CalledProcessError:
                exit()

        cpu_file.write('%f\n' % total_cpu)
        mem_file.write('%f\n' % total_memory)

        time.sleep(1)





