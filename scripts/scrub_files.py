#!/usr/bin/python

readfile = '/home/cokcybot/Downloads/underwater_ral/okvis_result/okvis_stereo_speedo1.csv'
writefile = '/home/cokcybot/Downloads/underwater_ral/okvis_result/okvis_stereo_speedo1.txt'
if __name__=='__main__':
    pkg_file = open(writefile, 'w+')

    with open(readfile) as f:
        f.readline()
        f.readline()
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            pkg_file.write('%s,%f,%f,%f,%f,%f,%f,%f\n' % (line[2], float(line[5]), float(line[6]), float(line[7]),
                                                        float(line[8]), float(line[9]), float(line[10]), float(line[11])))

    pkg_file.close()