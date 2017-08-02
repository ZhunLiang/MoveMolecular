import numpy as np
import re

MSD_file = open("MSD_charge_para.dat",'r')
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
