import pathlib

# some global vars for the c functions
WIDTH = 30
LEFT = 0
RIGHT = 1
FORWARD = FRONT = 2
BACKWARD = BACK = 3
STEP = 5

FILE = str(pathlib.Path().absolute() / "examples/basic.txt")

def read(path):
    lines = []
    with open(path, 'r') as file:

        while True:
            # Get next line from file
            line = file.readline().split(' ')
            if line == [] or line == ['']:
                break
            lines.append(line)
    return lines

def write(path, lines):
    data = [' '.join(str(word) for word in line) for line in lines]
    #data = [' '.join(i) for i in lines]
    data = [line + '\n' for line in data]
    with open(path, 'w') as file:
        file.writelines(data)

def parse(data):
    txt = ""
    for line in data:
        for v in line:
            if v == "R":
                txt += "R"
                continue
            value = int(v)
            if (value == 127): txt += "X"
            elif (value > 100): txt += "?"
            elif (value >= 1): txt += "."
            else: txt += " "
        txt += "\n"
    return txt

def clearFails():
    print('fails reset')
    lines = read(FILE)
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            lines[y][x] = str(abs(int(lines[y][x])))
    write(FILE, lines)

def fail(current, direction, distance):
    global STEP
    print("Path failed!")
    current = (int(round(current[0])), int(round(current[1])))
    data = []
    distance = int(round(distance))
    lines = read(FILE)
    if (direction == FORWARD):
        # Positive x
        p = (round(current[0] + distance), round(current[1] - (STEP)))
        for i in range(STEP * 2):
            if (p[1] + i < 0 or p[1] + i > len(lines)): continue;
            lines[p[1] + i][p[0]] = -int(lines[p[1] + i][p[0]])
    elif (direction == BACKWARD):
        # Negative x
        p = (current[0] - distance, round(current[1] - (STEP)))
        for i in range(STEP * 2):
            if (p[1] + i < 0 or p[1] + i > len(lines)): continue;
            lines[p[1] + i][p[0]] = -int(lines[p[1] + i][p[0]])
    elif (direction == LEFT):
        # Negative y
        p = (round(current[0] - (STEP)), current[1] - distance)
        for i in range(STEP * 2):
            if (p[0] + i < 0 or p[0] + i > len(lines[p[1]])): continue;
            lines[p[1]][p[0] + i] = -int(lines[p[1] + i][p[0]])
    elif (direction == RIGHT):
        # Positive y
        p = (round(current[0] - (STEP)), current[1] + distance)
        for i in range(STEP * 2):
            if (p[0] + i < 0 or p[0] + i > len(lines[p[1]])): continue;
            lines[p[1]][p[0] + i] = -int(lines[p[1] + i][p[0]])
    write(FILE, lines)

def cmark(current, direction, distance):
    global STEP
    current = (int(round(current[0])), int(round(current[1])))
    data = []
    distance = int(round(distance))
    lines = read(FILE)
    if (direction == FORWARD):
        # Positive x
        p = (round(current[0] + distance), round(current[1] - (STEP)))
        for i in range(STEP * 2):
            if (p[1] + i < 0 or p[1] + i > len(lines)): continue;
            lines[p[1] + i][p[0]] += STEP
            lines[p[1] + i][p[0]] = min(127, lines[p[1] + i][p[0]])
    elif (direction == BACKWARD):
        # Negative x
        p = (current[0] - distance, round(current[1] - (STEP)))
        for i in range(STEP * 2):
            if (p[1] + i < 0 or p[1] + i > len(lines)): continue;
            lines[p[1] + i][p[0]] += STEP
            lines[p[1] + i][p[0]] = min(127, lines[p[1] + i][p[0]])
    elif (direction == LEFT):
        # Negative y
        p = (round(current[0] - (STEP)), current[1] - distance)
        for i in range(STEP * 2):
            if (p[0] + i < 0 or p[0] + i > len(lines[p[1]])): continue;
            lines[p[1]][p[0] + i] += STEP
            lines[p[1]][p[0] + i] = min(127, lines[p[1]][p[0] + i])
    elif (direction == RIGHT):
        # Positive y
        p = (round(current[0] - (STEP)), current[1] + distance)
        for i in range(STEP * 2):
            if (p[0] + i < 0 or p[0] + i > len(lines[p[1]])): continue;
            lines[p[1]][p[0] + i] += STEP
            lines[p[1]][p[0] + i] = min(127, lines[p[1]][p[0] + i])
    write(FILE, lines)

clearFails()
