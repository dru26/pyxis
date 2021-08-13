from random import *
from math import *

map = [
"         BBBBBBBBBB                              ",
"         BxxxxxxxxBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
"         BxBBBBBBxB     .   B     .   B     .   B",
"         BxBBBBBBxB  BBBBBBBBBBBBBBBBBBBBBBBBBBBB",
"BBBBBBBBBBxx    xxB         B         B         B",
"BBB  xxx          B ... ... B ... ... B ... ... B",
"B   xBBBx   xxx   B . . . . B . . . . B . . . . B",
"BBB xBBBx  xBBBx  B . . . . B . . . . B . . . . B",
"B    xxx   xBBBx  B . . . . B . . . . B . . . . B",
"BBB        xBBBx  B . . . . B . . . .   . . . . B",
"BBB  xxx   xBBBx  B . . . . B . . . . B . . . . B",
"B   xBBBx   xxx   B . . . . B . . . . B . . . . B",
"BBB xBBBx         B . . . . B . . . . B . . . . B",
"B   xBBBx   xxx   B . . . . B . . . . B . . . . B",
"BBB  xxx   xBBBx  B . . . .   . . . . B . . . . B",
"BBB        xBBBx  B . . . . B . . . . B . . . . B",
"B    xxx   xBBBx  B . . . . B . . . . B . . . . B",
"BBB xBBBx  xBBBx  B . . . . B . . . . B . . . . B",
"B   xBBBx   xxx     . ... ..B . ... ..B . ... ..B",
"BBB  xxx          B         B         B         B",
"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
]



with open('basic.txt', 'w') as file:
    '''
    border = '127 ' * 99
    border += '127\n'
    lines = [border]
    for x in range(98 + (100 * 1)):
        line = '127 '
        for y in range(98 + (100 * 1)):
            line += str(floor(random() * 0.1 * 127)) + " "
        line += ' 127\n'
        lines.append(line)
    lines.append(border)
    file.writelines(lines)
    '''
    for i in range(len(map)):
        l1 = ""
        #l3 = ""
        for j in range(len(map[i])):
            #if (map[i][j] == " "):
                #l1 += str(floor(random() * 0.1 * 127)) + " "
                #l2 += str(floor(random() * 0.1 * 127)) + " "
                #l3 += str(floor(random() * 0.1 * 127)) + " "
            if (map[i][j] == "B"):
                l1 += "127 "
                #l3 += "127 "
            if (map[i][j] == " "):
                l1 += "0 "
                #l3 += "127 "
            if (map[i][j] == "."):
                l1 += "51 ";
                #l3 += str(floor(random() * 0.5 * 127)) + " ";
            if (map[i][j] == "x"):
                l1 += "101 ";
                #l3 += str(floor(random() * 0.8 * 127)) + " ";
        #file.writelines([l1[:-1] + "\n", l2[:-1] + "\n", l3[:-1] + "\n"])
        file.writelines([l1[:-1] + "\n"])
