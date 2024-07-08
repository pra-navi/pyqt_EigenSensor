import numpy as np
import time
import os
import json
from pyqtgraph.Qt import QtGui, QtCore
from frontend_classification import create_class, app, win, create_logo_label

# Initialise
refresh_interval_ms = 100
data_loaded_classification = np.zeros((4, 1))
classification_circle = np.zeros(4)
classification_circle[0] = 1

# Constantly refresh code
def stream():
    global data_loaded_classification, classification_circle

    # Constantly refresh values that have been changed on the frontend screen settings
    import frontend_classification
    import subprocess

    screen = frontend_classification.screen

    # Switch between screens
    if screen == 1:
        app.closeAllWindows()
        subprocess.call(["python", "backend_timeseries.py"])
    elif screen == 2:
        app.closeAllWindows()
        subprocess.call(["python", "backend_fft.py"])

    # Load values from frontend_classification
    model = frontend_classification.model
    isChanged = frontend_classification.isChanged
    output_control = frontend_classification.output_control
    control1_dropdown = frontend_classification.control1_dropdown
    control2_dropdown = frontend_classification.control2_dropdown
    control3_dropdown = frontend_classification.control3_dropdown
    control4_dropdown = frontend_classification.control4_dropdown
    bar1 = frontend_classification.bar1
    bar2 = frontend_classification.bar2
    bar3 = frontend_classification.bar3
    bar4 = frontend_classification.bar4

    spotify_options = ["Next Track", "Previous Track", "Play", "Pause", "Volume Up", "Volume Down"]
    other_options = ["1", "2", "3", "4"]

    # Update dropdowns based on the frontend screen settings
    if isChanged:
        frontend_classification.isChanged = False
        output_control = frontend_classification.output_control
        control1_dropdown = frontend_classification.control1_dropdown
        control2_dropdown = frontend_classification.control2_dropdown
        control3_dropdown = frontend_classification.control3_dropdown
        control4_dropdown = frontend_classification.control4_dropdown
        if output_control == 'Spotify':
            control1_dropdown.clear()
            for option in spotify_options:
                control1_dropdown.addItem(option)
            control2_dropdown.clear()
            for option in spotify_options:
                control2_dropdown.addItem(option)
            control3_dropdown.clear()
            for option in spotify_options:
                control3_dropdown.addItem(option)
            control4_dropdown.clear()
            for option in spotify_options:
                control4_dropdown.addItem(option)
        else:
            control1_dropdown.clear()
            for option in other_options:
                control1_dropdown.addItem(option)
            control2_dropdown.clear()
            for option in other_options:
                control2_dropdown.addItem(option)
            control3_dropdown.clear()
            for option in other_options:
                control3_dropdown.addItem(option)
            control4_dropdown.clear()
            for option in other_options:
                control4_dropdown.addItem(option)
    
    # Randomise and populate the dataset
    data_loaded_classification = np.random.rand(4,1)   
    data_loaded_classification = data_loaded_classification * 100
    classification_circle = np.zeros(4)
    classification_circle[data_loaded_classification.argmax()] = 1

    bar1.setValue(int(data_loaded_classification[0][0]))
    bar2.setValue(int(data_loaded_classification[1][0]))
    bar3.setValue(int(data_loaded_classification[2][0]))
    bar4.setValue(int(data_loaded_classification[3][0]))

    # Update the classification circle
    if classification_circle[0] == 1:
        frontend_classification.circle1.setPixmap(QtGui.QPixmap("./images/lighted.png").scaled(50, 50))
        frontend_classification.circle2.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle3.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle4.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
    elif classification_circle[1] == 1:
        frontend_classification.circle1.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle2.setPixmap(QtGui.QPixmap("./images/lighted.png").scaled(50, 50))
        frontend_classification.circle3.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle4.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
    elif classification_circle[2] == 1:
        frontend_classification.circle1.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle2.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle3.setPixmap(QtGui.QPixmap("./images/lighted.png").scaled(50, 50))
        frontend_classification.circle4.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
    elif classification_circle[3] == 1:
        frontend_classification.circle1.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle2.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))  
        frontend_classification.circle3.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle4.setPixmap(QtGui.QPixmap("./images/lighted.png").scaled(50, 50))
    else:
        frontend_classification.circle1.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle2.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle3.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))
        frontend_classification.circle4.setPixmap(QtGui.QPixmap("./images/greyed.png").scaled(50, 50))

    # This is how to import the screen settings to use in backend code
    isBandPass = frontend_classification.isBandPass
    isBandStop = frontend_classification.isBandStop
    if isBandPass and not isBandStop:
        type = "bandpass"
    elif isBandStop and not isBandPass:
        type = "bandstop"
    # print(type)

    notch = frontend_classification.notch
    # print(notch)


timer = QtCore.QTimer()
timer.timeout.connect(stream)
timer.start(refresh_interval_ms)

win.show()

app.exec_()

