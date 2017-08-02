import re

#str1 = r"\A(\s+)(\d+\w+)(\s+)(.+)(\s+)(\d+)(\s+)(?P<id1>\-?\d+)(\s+)(?P<id2>\-?\d+)(\s+)(?P<id3>\-?\d+) \8"
#str1 = r"\A(\s+)(\d+\w+)(\s+)(.+)(\s+)(\d+)(\s+)(?P<id1>\-?\d+.*)(\s+)"
str2 = r"\s+(\-?\S+)\s+(\-?\S+)\s+(\-?\S+)\s+(\-?\S+)\s+(\-?\S+)\s+(\-?\S+)"
X_box = ["1","2","3"]
Y_box = ["2","4","6"]
Z_box = ["3","6","9"]
str1 = r"(\-?\d+\.\d+)"
string1 = "    1PC      C2    1   0.093   1.161   1.316 -0.1734 -0.1528 -0.0993"
re_str1 = re.compile(str1)
list = [X_box,Y_box,Z_box]
i = 0
j = 0

m = re.match(str2 , string1)
print m.group(1)

def replace(match):
    global i, list, j
    rep1 = list[i]
    rep2 = rep1[j]
    i += 1
    return rep2
#pat = re.compile(str1)
#replace_str = pat.sub(replace, string1,3)
#replace_str = re.sub(str1 , replace() , string1)

#print replace_str



