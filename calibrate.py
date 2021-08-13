#import bindings
import pathlib
import PySimpleGUI as sg
import extra

DUMMY = str(pathlib.Path().absolute() / "examples/blank.txt")
ACTUAL = str(pathlib.Path().absolute() / "examples/basic.txt")

def goToFake():
    pass

def callibrate():
    pass
    x = 0
    y = 0

real_map = extra.parse(extra.read(ACTUAL))
print(real_map)
layout = [
    [
    sg.Text("", font = "Courier 14", size = (6,1), key="-B0-", text_color = "black"),
    sg.Text(text = real_map, font = "Courier 14")
    ]
]


x = 0
y = 0

if __name__ == "__main__":
	# Create the window
    window = sg.Window("Python ", layout, resizable = True)
    while True:
        event, values = window.read(100)
        data = extra.read(DUMMY)
        data[y][x] = "R"
        map = extra.parse(data)
        window["-B0-"].update(map)
        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break
