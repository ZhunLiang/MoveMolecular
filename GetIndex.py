import numpy as np

input_parameter = {"input_file":"test2 .gro","output_file":"test2.txt","box_size":"0.5-0.5-0.5"}

def GetInput(file_name):
    file = open(file_name)
    lines = file.readlines()
    row = len(lines)
    Coor = np.zeros([3,row-3])
    Res_name = []
    Atom_name = []
    Atom_index =np.zeros(row-3)
    Box_size = np.array(lines[row - 1].split())
    for i in range(2,row-1):
        Res_name.append(lines[i].split()[0])
        Atom_name.append(lines[i].split()[1])
        Atom_index[i - 2] = np.array(int(lines[i].split()[2]))
        Coor[0, i - 2] = np.array(float(lines[i].split()[3]))
        Coor[1, i - 2] = np.array(float(lines[i].split()[4]))
        Coor[2, i - 2] = np.array(float(lines[i].split()[5]))
    return Res_name,Atom_name,Atom_index,Coor

Res_name,Atom_name,Atom_index,Coor = GetInput(input_parameter['input_file'])

def MatchIndex(dim , distance):
    match_Index = Atom_index[Coor[dim , :] > distance]
    #print match_Index
    #match_Coor = Coor[dim , match_Index - 1]
    return match_Index

match_Index = MatchIndex(0,0.2)
