"""
from socha import *

import logging
import random
import cProfile
import pstats

from extention import *
from utils import *

test = [None, "Lol", 12, None, 69]

for each in test:
    if each:
        print(True)
    else:
        print(False)"""
"""
def other_recursive(n, bool = True, dict={}):
    if n == 0:
        return 1
    
    dict[n] = n
    other_recursive(n-1, False)
    if bool:
        return dict
    

def t(length, result = [], d = {}):
    if length == 10:
        return
    else:
        result.append(length)   #list.append
        d[length] = length + 1  #dict.append
        t(length + 1)           #do again

    return (result, d)          #return above

#x, y = t(0)
#print(x, y)

def test(length, result: list = [], d = {}):
    if length == 4:
        return
    else:
        result.remove(length)   #list.remove
        del d[length]
        test(length + 1, result, d)           #do again

    return (result, d)          #return above

list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
list2 = {0: 0,
         1: 1,
         2: 2,
         3: 3,
         4: 4,
         5: 5}

x, y = test(0, list1, list2)
print(x, y)
list = [0,1,2,3,4,5]
print(range(5))
for i in range(1,7):
    index = i%6-1
    print()
    print("each+1",list[index+1])
    print("each",list[index])
    print("each-1",list[index-1])

dict1 = {"69": [1]}
dict2 = {"69": [2, 3]}
dict3 = {}
for each in dict1:
    if each in dict2:
        print(each)
        value = dict1[each]
        value2 = dict2[each]
        value.extend(value2)
        dict3[each] = value
    else:
        dict3[each] = dict1[each]
for each in dict2:
    if not each in dict3:
        dict3[each] = dict2[each]
print(dict3)

for i in range(0,6):
    print(i)
    print()
    print("each+1",list[(i+1) % 6 ])
    print("each",list[(i) % 6])
    print("each-1",list[(i-1) % 6])
"""

cool_list = [1,2,3,4,5,6,7,9]
not_cool_list= [10,11,12]
super_list = []
super_list.extend(cool_list)
super_list.extend(not_cool_list)
print(super_list)