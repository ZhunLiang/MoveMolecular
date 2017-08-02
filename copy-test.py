import re


def replace(match):
    global i, list
    rep = list[i]
    i += 1
    return rep


str = '1 adfa fa 2 fafsa 3 adfaf'
list = ['1', 'two', 'three']

pat = re.compile(r'\d+')
i = 0

print pat.sub(replace, str)
