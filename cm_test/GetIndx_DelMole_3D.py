import numpy as np
import re
import sys
import shutil
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", dest = "gro_file", default = "LWO-SOL-3_7-2.gro", help = "input gro file, default start.gro")
parser.add_option("-n", dest = "index_file", default = "index.ndx", help = "input index file, default index.ndx")
parser.add_option("--add", dest = "Add_index_name", default = "NEW_index", help = "Add index name, default NEW_index")
parser.add_option("--dim", dest = "Dim", type = "string",default = "0 0 1", help = '''three number,x y z, 0 or 1, 0 means don't calculate this dimension,ep:"0 0 1"''')
parser.add_option("--low", dest = "Dmin", type = "string",default = "-1 -1 0", help = '''min value at dimension x y z, ep:"3 3.5 3"''')
parser.add_option("--up", dest = "Dmax", type = "string",default = "999 999 1", help = '''max value at dimension x y z, ep:"8 8.5 8"''')
parser.add_option("--NCM", dest = "n_NCM", type = "int",default = 0, help = "center of molecule\n0: number; 1: charge; 2: mass")
parser.add_option("--nStart1", dest = "nStart1", type = "int",default = 10260, help = "Need to delete molecular, start number of atoms in gro file")
parser.add_option("--nm1", dest = "nm1", type = "int",default = 9140, help = "Number of molecules total number")
parser.add_option("--tN1", dest = "tN1", type = "int",default = 1, help = "the type of needed to delete molecule")
parser.add_option("--on", dest = "output_index", default = None, help = "output index file, default no output index.ndx")
parser.add_option("--og", dest = "output_gro", default = None, help = "input index file, default no output gro file")

#test_args = ['-i','solid_water.gro','--dim','1 1 1','--low','3 3.5 3','--up','8.85 8.85 5.55','--nStart1','5130','--nm1','38052','--tN1','6','--og','output.gro']
#(options, args) = parser.parse_args(test_args)
(options, args) = parser.parse_args()


Dim = options.Dim
Dmin = options.Dmin
Dmax = options.Dmax
Add_index = options.Add_index_name
index_file = options.index_file
gro_file = options.gro_file
n_NCM = options.n_NCM
nStart1 = options.nStart1
nm1 = options.nm1
tN1 = options.tN1
gen_index = 0
output_ndx = options.output_index
output_gro = options.output_gro

'''
Dim = "1 1 1"
Dmin = "3 3.5 3"
Dmax = "8.85 8.85 5.55"
Add_index = "IN_MICA"
gro_file = r"E:\Simulation\Code\Wrinting\python\MoveMolecular\cm\solid_water.gro"
index_file = r"E:\Simulation\Zhoujun\MD\Mica\lz\no_fix\index.ndx"
n_NCM = 0
nStart1 = 5130
nm1 = 38052
tN1 = 6
output_ndx = None#r"E:\Simulation\Zhoujun\MD\Mica\lz\no_fix\index2.ndx"#None#"output.ndx"
output_gro = r"E:\Simulation\Code\Wrinting\python\MoveMolecular\cm\output.gro"
'''
#--------------------------------------initial parameter--------------------------------------#
dim_matrix = np.array([int(Dim.split()[i]) for i in range(len(Dim.split()))])
dim_number = np.sum(dim_matrix)
low_matrix = np.array([float(Dmin.split()[i]) for i in range(len(Dmin.split()))])
up_matrix = np.array([float(Dmax.split()[i]) for i in range(len(Dmax.split()))])
low_dim = np.zeros([3])
low_compare = np.zeros([3])   #used for compare
up_compare = np.zeros([3])    #used for compare
for i in range(3):
    if dim_matrix[i] <= 0:
        low_compare[i] = -999999.0
        up_compare[i] = 999999.0
    else:
        low_compare[i] = low_matrix[i]
        up_compare[i] = up_matrix[i]
#------------------------load MSD_charge_para.dat--------------------------#
try:
    MSD_file = open(r"MSD_charge_para.dat",'r')
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
    #print numAt[i]
    for j in range(int(numAt[i])):
        atNCM[0][i][j] = float(re_match_atomN.findall(MSD_data)[atom_index])
        #print atNCM[0][i][j]
        atNCM[1][i][j] = float(re_match_atomC.findall(MSD_data)[atom_index])
        #print atNCM[1][i][j]
        atNCM[2][i][j] = float(re_match_atomM.findall(MSD_data)[atom_index])
        #print atNCM[2][i][j]
        if atNCM[0][i][j] > 0:
            atNCM[0][i][j] = 1.0
        else:
            atNCM[0][i][j] = 0.0
        atom_index += 1
MSD_file.close()
#--------------------total mass/effective number/charge in a whole molecule ------------------#
mol_NCM = np.zeros([3,nType])
for j in range(nType):
    for k in range(3):
        mol_NCM[k][j] = 0.0
        mol_NCM[k][j] = np.sum(atNCM[k][j][0:-1])
        if abs(mol_NCM[k][j]<1e-6):
            mol_NCM[k][j] = 1.0
        #print mol_NCM[k][j]

#------------------------------------------Get the position and box size from gro file ---------------------------#
coor_match = r"-?\d+\.\d+" #match coordinate
re_match = re.compile(coor_match)
file = open(gro_file,'r')
lines = file.readlines()
rows = len(lines)
Atom_num = int(lines[1])
Coordinate = np.zeros([3,Atom_num])
for i in range(Atom_num):
    Coordinate[0, i] = np.array(float(re_match.findall(lines[i + 2])[0]))
    Coordinate[1, i] = np.array(float(re_match.findall(lines[i + 2])[1]))
    Coordinate[2, i] = np.array(float(re_match.findall(lines[i + 2])[2]))
Box = np.zeros([3])
for i in range(3):
    Box[i] = float(lines[-1].split()[i])
    #print Box[i]
totNum = int(lines[1].split()[0])
#print totNum
file.close()

#-----------------------------------------------generate new index---------------------------#
if output_ndx != None:
    shutil.copy(index_file, output_ndx)
    index_open = open(output_ndx, 'a')
    index_open.write('\n[ %s ]\n' % Add_index)
    index = 0
    for i in range(Atom_num):
        if all(Coordinate[:,i]>=low_compare) and all(Coordinate[:,i]<=up_compare):
            index_open.write(" " + str(i + 1))
            index += 1
            if (index) % 15 == 0:
                index_open.write('\n')
    index_open.write('\n')
    index_open.close()

#---------------------------------load position-------------------------------------#
def load_position(atom_coor, nm, atoms, nStart, Lbox):
    halfLbox = Lbox/2.0
    tmpPos = np.zeros([3])
    posmolecule = np.zeros([nm, atoms, 3])
    for i in range(nm):
        molN = nStart+i*atoms
        for j in range(atoms):
            for k in range(3):
                tmpPos[k] = atom_coor[k][molN+j]
                #while tmpPos[k]-atom_coor[k][molN]> halfLbox[k]:
                #    tmpPos[k] -= Lbox[k]
                #while tmpPos[k]-atom_coor[k][molN]< halfLbox[k]:
                #    tmpPos[k] += Lbox[k]
                posmolecule[i][j][k] = tmpPos[k]
    return posmolecule

#----------------------------get molecular center and delete molecular atoms index-----------------------------------#
tN1 -= 1
atoms1 = int(numAt[tN1])
pos1 = load_position(Coordinate, nm1, atoms1, nStart1, Box)
center_f = np.zeros([3,nm1])
del_mol_num = 0
del_index = np.zeros([nm1*atoms1])
index_del = 0

for i in range(nm1):
    for k in range(3):
        for m in range(atoms1):
            center_f[k][i] += pos1[i][m][k]*atNCM[n_NCM][tN1][m]
        center_f[k][i] /= mol_NCM[n_NCM][tN1]

for i in range(nm1):
    if all(center_f[:,i]>=low_compare) and all(center_f[:,i]<=up_compare):
        del_mol_num += 1
        for n in range(atoms1):
            del_index[index_del] = nStart1+i*atoms1+n+1
            index_del += 1
            #print del_index[i*atoms1+n]
#print del_mol_num
tot_mol_delete = del_mol_num*atoms1

#-------------------------------------------delete molecular-------------------------------------------#
if output_gro != None:
    output_gro_file = open(output_gro,"w")
    j = 0
    lines[1] = str(int(lines[1])-tot_mol_delete)+'\n'
    for i in range(rows):
        new_index = i-1
        if  j < tot_mol_delete:
            if new_index == del_index[j]:
                j += 1
            else:
                output_gro_file.write(lines[i])
        else:
            output_gro_file.write(lines[i])
    output_gro_file.close()

