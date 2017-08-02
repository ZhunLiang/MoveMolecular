import numpy as np
import re
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", dest = "gro_file", default = "start.gro", help = "input gro file, default start.gro")
parser.add_option("-n", dest = "index_file", default = "index.ndx", help = "input index file, default index.ndx")
parser.add_option("-A", dest = "Add_index_name", default = "NEW_index", help = "Add index name, default NEW_index")
parser.add_option("-d", dest = "Dim", type = "int",default = 2, help = "dimension for get atom index, 0 means x, 1 means y, 2 means z, default 2")
parser.add_option("-l", dest = "Dmin", type = "float",default = 0.0, help = "min value at dimension, default 0")
parser.add_option("-r", dest = "Dmax", type = "float",default = 2.0, help = "min value at dimension, default 2")
(options, args) = parser.parse_args()


Dim = options.Dim
Dmin = options.Dmin
Dmax = options.Dmax
Add_index = options.Add_index_name
index_file = options.index_file
gro_file = options.gro_file
#Dim = 2
#Dmin = 9.059
#Dmax = 13.737
#Add_index = "In_LWO"
#gro_file = r"E:\Simulation\Zhoujun\MD\Li2W4O13\test\start.gro"
#index_file = r"E:\Simulation\Zhoujun\MD\Li2W4O13\test\index.ndx"

#------------------------load MSD_charge_para.dat--------------------------#
try:
    MSD_file = open("MSD_charge_para.dat",'r')
except:
    print "\nNOTE: Parameter file cannot be loaded, mission terminated.\n"
    sys.exit()

MSD_data = MSD_file.read()
match_type = r"^\w+\S*\s+(\d+)"
match_atomN = r"(\d+)\s+\S+\.\d+\s+\S+\.\d+$"
match_atomC = r"\d+\s+(\S+\.\d+)\s+\S+\.\d+$"
match_atomM = r"\d+\s+\S+\.\d+\s+(\S+\.\d+)$"
re_match_type = re.compile(match_type, re.M)
re_match_atomN = re.compile(match_atomN, re.M)
re_match_atomC = re.compile(match_atomC, re.M)
re_match_atomM = re.compile(match_atomM, re.M)
nType = int(re_match_type.findall(MSD_data)[0])
numAt = np.zeros([nType])
atNCM = np.zeros([3,nType,100])
atom_index = 0
for i in range(nType):
    numAt[i] = int(re_match_type.findall(MSD_data)[i+1])
    for j in range(int(numAt[i])):
        atNCM[0][i][j] = float(re_match_atomN.findall(MSD_data)[atom_index])
        atNCM[1][i][j] = float(re_match_atomC.findall(MSD_data)[atom_index])
        atNCM[2][i][j] = float(re_match_atomM.findall(MSD_data)[atom_index])
        if atNCM[0][i][j] > 0:
            atNCM[0][i][j] = 1.0
        else:
            atNCM[0][i][j] = 0.0
        atom_index += 1
MSD_file.close()

#-----------------------------------------------generate new index---------------------------#
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
        if (index+1)%15 == 0:
            index_open.write('\n')
index_open.write('\n')
index_open.close()