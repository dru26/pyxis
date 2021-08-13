#import bindings
import pathlib
import PySimpleGUI as sg
import extra
import bindings
import math
import random
import copy
DUMMY = str(pathlib.Path().absolute() / "examples/blank.txt")
ACTUAL = str(pathlib.Path().absolute() / "examples/basic.txt")

extra.setStep(1)

CPOS = (0, 0)

DATA = []
for i in range(50):
    line = []
    for j in range(50):
        line.append('0')
    DATA.append(line)

extra.write(DUMMY, DATA)

MX = 13
MY = 11

O = 14

random.seed(12)

real_map_data = extra.read(ACTUAL)
real_map = extra.parse(real_map_data)

POOL = []
SIZE = 3
FOUND = -1
FAILS = 0
def callibrate():
    global POOL, SIZE, FOUND, real_map_data, MX, MY, CPOS, O, FAILS
    if len(POOL) == 0 and bindings.hasPosition() == False:
        if FOUND == 0:
            FAILS += 1
            if FAILS > 3:
                if FAILS == 3:
                    print("DONE")
                # NORMALIZE
                # END CALLIBRATION
                return
        else:
            FAILS = 0
        corner = math.ceil(SIZE / 2)
        POOL.append((corner, corner))
        POOL.append((-corner, corner))
        POOL.append((corner, -corner))
        POOL.append((-corner, -corner))
        for i in range(SIZE):
            POOL.append((-corner, -corner + i))
            POOL.append((-corner + i, -corner))
            POOL.append((corner, -corner + i))
            POOL.append((-corner + i, corner))
        FOUND = 0
        SIZE += 1

    # MOVE
    elif bindings.hasPosition():
        point = bindings.nextPosition()
        point = (point[0] - O, point[1] - O)
        rpoint = (point[0] + MX, point[1] + MY)
        v = 0
        try:
            v = 127 - int(real_map_data[rpoint[1]][rpoint[0]])
        except IndexError:
            pass
        if v > random.randint(0, 127):
            # IF free, move here
            CPOS = point
            point = (point[0] + O, point[1] + O)
            FOUND += 1
            DATA[point[1]][point[0]] = str(max(int(DATA[point[1]][point[0]]) - 100, 0))
        else:
            # Else, mark it as blocked and remove the path
            while bindings.hasPosition():
                bindings.nextPosition()
            point = (point[0] + O, point[1] + O)
            DATA[point[1]][point[0]] = str(min(int(DATA[point[1]][point[0]]) + 50, 127))
    else:
        random.shuffle(POOL)
        point = POOL.pop()
        if random.randint(0, 2) == 0:
            POOL.insert(0, point)
        bindings.findPath((CPOS[0] + O, CPOS[1] + O), (point[0] + O, point[1] + O), DUMMY)
        if not bindings.hasPosition():
            point = (point[0] - O, point[1] - O)
            fpoint = (point[0] - MX, point[1] - MY)
            fpoint = (fpoint[0] + O, fpoint[1] + O)
            DATA[fpoint[1]][fpoint[0]] = str(min(int(DATA[fpoint[1]][fpoint[0]]) + 50, 127))
            #print("ERR")
    # Update the file
    #print(len(POOL))
    extra.write(DUMMY, DATA)



layout = [
    [
    sg.Text("", font = "Courier 14", key="-B0-", text_color = "black"),
    sg.Text(text = real_map, font = "Courier 14")
    ]
]

if __name__ == "__main__":
	# Create the window
    window = sg.Window("Python ", layout, resizable = True)
    while True:
        event, values = window.read(1)
        v = DATA[CPOS[1] + O][CPOS[0] + O]
        DATA[CPOS[1] + O][CPOS[0] + O] = "R"
        map = extra.parse(DATA)
        print(map)
        DATA[CPOS[1] + O][CPOS[0] + O] = v
        callibrate()
        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break
