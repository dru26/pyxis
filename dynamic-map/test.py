from random import *
from math import *

map = [
"         BBBBBBBBBB          ",
"         BxxxxxxxxBBBBBBBBBBB",
"         BxBBBBBBxB     .   B",
"         BxBBBBBBxB  BBBBBBBB",
"BBBBBBBBBBxx    xxB         B",
"BBB  xxx          B ... ... B",
"B   xBBBx   xxx   B . . . . B",
"BBB xBBBx  xBBBx  B . . . . B",
"B    xxx   xBBBx  B . . . . B",
"BBB        xBBBx  B . . . . B",
"BBB  xxx   xBBBx  B . . . . B",
"B   xBBBx   xxx   B . . . . B",
"BBB xBBBx         B . . . . B",
"B   xBBBx   xxx   B . . . . B",
"BBB  xxx   xBBBx  B . . . . B",
"BBB        xBBBx  B . . . . B",
"B    xxx   xBBBx  B . . . . B",
"BBB xBBBx  xBBBx  B . . . . B",
"B   xBBBx   xxx     . ... ..B",
"BBB  xxx          B         B",
"BBBBBBBBBBBBBBBBBBBBBBBBBBBB"
]

with open('map.txt', 'w') as file:
    for i in range(len(map)):
        l1 = ""
        l2 = ""
        l3 = ""
        for j in range(len(map[i])):
            if (map[i][j] == " "):
                l1 += str(floor(random() * 0.1 * 127)) + " "
                l2 += str(floor(random() * 0.1 * 127)) + " "
                l3 += str(floor(random() * 0.1 * 127)) + " "
            if (map[i][j] == "B"):
                l1 += "127 "
                l2 += "127 "
                l3 += "127 "
            if (map[i][j] == "B"):
                l1 += "127 "
                l2 += "127 "
                l3 += "127 "
            if (map[i][j] == "B"):
                l1 += str(floor(random() * 0.5 * 127)) + " ";
                l2 += str(floor(random() * 0.5 * 127)) + " ";
                l3 += str(floor(random() * 0.5 * 127)) + " ";
            if (map[i][j] == "x"):
                l1 += str(floor(random() * 0.8 * 127)) + " ";
                l2 += str(floor(random() * 0.8 * 127)) + " ";
                l3 += str(floor(random() * 0.8 * 127)) + " ";
        file.writelines([l1[:-1] + "\n", l2[:-1] + "\n", l3[:-1] + "\n"])
