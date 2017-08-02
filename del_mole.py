import numpy as np
import re
import sys, getopt
from optparse import OptionParser

Dim = 2
Dmin = 26.25
Dmax = 36
Add_index = "In_LWO"
gro_file = "test2-4-2e.gro"
index_file = "index.ndx"
index_open = open(index_file, 'a')
index_open.write('\n[ %s ]\n'%Add_index)
coor_match = r"-?\d+\.\d+" #match coordinate
re_match = re.compile(coor_match)
file = open(gro_file,'r')
lines = file.readlines()
rows = len(lines)
Atom_num = int(lines[1])
Coordinate = np.zeros([3,Atom_num])
index = 0
for i in range(Atom_num):
    Coordinate[0, i] = np.array(float(re_match.findall(lines[i + 2])[0]))
    Coordinate[1, i] = np.array(float(re_match.findall(lines[i + 2])[1]))
    Coordinate[2, i] = np.array(float(re_match.findall(lines[i + 2])[2]))
    if Coordinate[Dim, i] >= Dmin and Coordinate[Dim, i] <= Dmax:
        index_open.write(" " + str(i+1))
        index += 1
        if index == 1:
            INDEX = np.array([i+1])
        else:
            INDEX = np.append(INDEX,i+1)
        if index%15 == 0:
            index_open.write('\n')
index_open.write('\n')
index_open.close()

new_gro = "test2-4-3e.gro"
new_gro_file = open(new_gro,"w")
j = 0
for i in range(rows):
    new_index = i-1
    if j < len(INDEX):
        if new_index == INDEX[j]:
            j += 1
        else:
            new_gro_file.write(lines[i])
    else:
        new_gro_file.write(lines[i])

new_gro_file.close()