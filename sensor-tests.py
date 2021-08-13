import PySimpleGUI as sg
from rio.pins import sonar_right, sonar_left, motor_FL
from rio.pins import motor_BR, motor_BL, motor_FR, ir_FL, ir_BL, ir_FR, ir_BR
from rio.pins import power, table1, table2, table3, table4, table5, table6
import asyncio

sg.theme('dark grey 9')

layout = [
    [sg.Text("Power Button: "), sg.Text(size = (40,1), key="-B0-", text_color = "red")],
    [
        sg.Text("Table 1 Button: "), sg.Text(size = (12,1), key="-B1-", text_color = "red"),
        sg.Text("Table 2 Button: "), sg.Text(size = (12,1), key="-B2-", text_color = "red"),
        sg.Text("Table 3 Button: "), sg.Text(size = (12,1), key="-B3-", text_color = "red")
    ],
    [
        sg.Text("Table 4 Button: "), sg.Text(size = (12,1), key="-B4-", text_color = "red"),
        sg.Text("Table 5 Button: "), sg.Text(size = (12,1), key="-B5-", text_color = "red"),
        sg.Text("Table 6 Button: "), sg.Text(size = (12,1), key="-B6-", text_color = "red")
    ],

    [sg.Text("", size = (40,1))],
    [
        sg.Text("FRONT LEFT", size = (52,1), text_color = "yellow"),
        sg.Text("FRONT RIGHT", size = (50,1), text_color = "yellow")
    ],
    [
        [
            sg.Button("FL Motor Power (Forward)", size = (48,1)),
            sg.Button("FR Motor Power (Forward)", size = (50,1))
        ],
        [
            sg.Button("FL Motor Power (Backward)", size = (48,1)),
            sg.Button("FR Motor Power (Backward)", size = (50,1))
        ],
        [
            sg.Text("IR: ", size = (10,1)), sg.Text(size = (40,1), key="-I1-", text_color = "red"),
            sg.Text("IR: ", size = (10,1)), sg.Text(size = (40,1), key="-I2-", text_color = "red")
        ],
        [
            sg.Text("Motor: ", size = (10,1)), sg.Text(size = (40,1), key="-M1-", text_color = "red"),
            sg.Text("Motor: ", size = (10,1)), sg.Text(size = (40,1), key="-M2-", text_color = "red")
        ]
    ],
    [
        sg.Text("BACK LEFT", size = (52,1), text_color = "yellow"),
        sg.Text("BACK RIGHT", size = (50,1), text_color = "yellow")
    ],
    [
        [
            sg.Button("BL Motor Power (Forward)", size = (48,1)),
            sg.Button("BR Motor Power (Forward)", size = (50,1))
        ],
        [
            sg.Button("BL Motor Power (Backward)", size = (48,1)),
            sg.Button("BR Motor Power (Backward)", size = (50,1))
        ],
        [
            sg.Text("IR: ", size = (10,1)), sg.Text(size = (40,1), key="-I3-", text_color = "red"),
            sg.Text("IR: ", size = (10,1)), sg.Text(size = (40,1), key="-I4-", text_color = "red")
        ],
        [
            sg.Text("Motor: ", size = (10,1)), sg.Text(size = (40,1), key="-M3-", text_color = "red"),
            sg.Text("Motor: ", size = (10,1)), sg.Text(size = (40,1), key="-M4-", text_color = "red")
        ]
    ],

    [sg.Text("", size = (40,1))],
    [
        sg.Text("LEFT SONAR", size = (52,1), text_color = "yellow"),
        sg.Text("RIGHT SONAR", size = (50,1), text_color = "yellow")
    ],
    [
        sg.Text("Value: ", size = (10,1)), sg.Text(size = (40,1), key="-S3-", text_color = "red"),
        sg.Text("Value: ", size = (10,1)), sg.Text(size = (40,1), key="-S4-", text_color = "red")
    ],

]

if __name__ == "__main__":
	# Create the window
    window = sg.Window("Python ", layout, resize = True)

	# Create an event loop
    while True:
        event, values = window.read(100)
        # Update the Button values
        window["-B0-"].update(str(power.is_pressed))
        window["-B1-"].update(str(table1.is_pressed))
        window["-B2-"].update(str(table2.is_pressed))
        window["-B3-"].update(str(table3.is_pressed))
        window["-B4-"].update(str(table4.is_pressed))
        window["-B5-"].update(str(table5.is_pressed))
        window["-B6-"].update(str(table6.is_pressed))

        # Update the IR sensor values
        window["-I1-"].update(str(ir_FL.value))
        window["-I2-"].update(str(ir_FR.value))
        window["-I3-"].update(str(ir_BL.value))
        window["-I4-"].update(str(ir_BR.value))

        # Update the Motor values
        window["-M1-"].update(str(motor_FL.value))
        window["-M2-"].update(str(motor_FR.value))
        window["-M3-"].update(str(motor_BL.value))
        window["-M4-"].update(str(motor_BR.value))

        # Update the Sonar values
        window["-S3-"].update(sonar_left.value)
        window["-S4-"].update(sonar_right.value)

        # Read Motor button presses
        if event == "BL Motor Power (Forward)":
            motor_BL.forward()
        elif event == "BL Motor Power (Backward)":
            motor_BL.backward()
        else:
            motor_BL.stop()

        if event == "FL Motor Power (Forward)":
            motor_FL.forward()
        elif event == "FL Motor Power (Backward)":
            motor_FL.backward()
        else:
            motor_FL.stop()

        if event == "BR Motor Power (Forward)":
            motor_BR.forward()
        elif event == "BR Motor Power (Backward)":
            motor_BR.backward()
        else:
            motor_BR.stop()

        if event == "FR Motor Power (Forward)":
            motor_FR.forward()
        elif event == "FR Motor Power (Backward)":
            motor_FR.backward()
        else:
            motor_FR.stop()

        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break

    window.close()
