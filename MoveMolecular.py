# ParaMeter
import GL
input_parameter = {"input_file":"","output_file":"","box_size":""}

i = 0 # i = 0,1,2
j = 0 # j = line for X_Coordinate

# input by command line
import sys, getopt
opts, args = getopt.getopt(sys.argv[1:], 'hi:o:b:')
 # -i input file,-o output file
for op , value in opts:
    if op == "-i":
        input_parameter["input_file"] = value
    elif op == "-o":
        input_parameter["output_file"] = value
    elif op == "-b":
#        print "-b is OK"
        input_parameter["box_size"] = value
    elif op == "-h":
        print '''
                 -i   input file;
                 -o   output file
                 -b   box size
                 -h   help'''

# get the input file(.gro) parameter, resname and x,y,z coordinate
def GetInputFile(file_name):
    import GL
    file = open(file_name)
    lines = file.readlines()
    row = len(lines)
    Box_Size = lines[row-1].split()
    for i in range(3,row):
        GL.Resname.append(lines[i - 1].split()[0])
        GL.X_Coordinate.append(lines[i - 1].split()[3])
        GL.Y_Coordinate.append(lines[i - 1].split()[4])
        GL.Z_Coordinate.append(lines[i - 1].split()[5])
    return

# replace X(Y,Z)_Coordinate by new_X(Y,Z)_Coordinate
def replace_coor(match):
    global i , j
    rep1 = new_Coordinate[i]
    print rep1
    rep2 = rep1[j]
    #print rep2
    if "-" in match.group():
        if "-" in rep2:
            return rep2
        else:
            rep2 = " "+rep2
    elif "-" in rep2:
        return rep2
    else:
        rep2 = " " + rep2
    i += 1
    return rep2

#replace box size
def replace_box(match):
    import GL
    global i
    rep = GL.new_Box_Size[i]
    i += 1
    return rep

# generate output file
def GenerOutputFile(file_name):
    import  shutil, re , GL
    global i , j
    str1 = r"((\-|\s)\d+\.\d?)" #match coordinate
    str2 = r"(\d+\.?\d+)" #match box
    re_str1 = re.compile(str1)
    re_str2 = re.compile(str2)
    shutil.copyfile(input_parameter["input_file"],file_name)
    file = open(file_name)
    lines = file.readlines()
    row = len(lines)
    # next is replace Coordinate
    for k in range(3,row):
        lines[k - 1] = re_str1.sub(replace_coor, lines[k - 1], 3)
        i = 0
        j += 1
    lines[row - 1] = re_str2.sub(replace_box, lines[row - 1], 3)
    open(file_name,"w").writelines(lines)
    return

#test initial new_Coordinate
input_parameter = {"input_file":"test.txt","output_file":"test2.txt","box_size":"0.5-0.5-0.5"}
GetInputFile(input_parameter["input_file"])
GL.new_X_Coordinate = GL.Y_Coordinate
print GL.new_X_Coordinate
GL.new_Y_Coordinate = GL.Z_Coordinate
print GL.new_Y_Coordinate
GL.new_Z_Coordinate = GL.X_Coordinate
print GL.new_Z_Coordinate
GL.new_Box_Size = input_parameter["box_size"].split("-")
new_Coordinate = [GL.new_X_Coordinate, GL.new_Y_Coordinate, GL.new_Z_Coordinate]
GenerOutputFile(input_parameter["output_file"])
# initial over