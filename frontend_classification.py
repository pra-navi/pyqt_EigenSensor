import numpy as np
import os
import datetime
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QLabel, QDockWidget, QLineEdit
from PyQt5.QtWidgets import QRadioButton, QButtonGroup, QComboBox, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from settings import settings_pop_up

# Initialization
refresh_interval_ms = 100
curves = []
plots = []
isLossOfData = False
screen = 3
output_control = 'Spotify'
model = 1
isChanged = False
control1 = 'Next Track'
control2 = 'Next Track'
control3 = 'Next Track'
control4 = 'Next Track'
isCircle1 = False
isCircle2 = False
isCircle3 = False
isCircle4 = False
isBandPass = True
isBandStop = False
notch = '50'

# Create the application and set its layout
app = QtWidgets.QApplication([])
win = QtWidgets.QMainWindow()
win.setWindowTitle("EigenSensor")
win.resize(1000, 1000)

central_widget = QWidget()
layout = QVBoxLayout()
central_widget.setLayout(layout)
central_widget.setStyleSheet("background-color: white;")
win.setCentralWidget(central_widget)

# Function to toggle the menubar
def toggle_menubar():
    if menubar.isVisible():
        menubar.hide()
    else:
        menubar.show()

# Function to make the window appear in the center of the screen
def center_window(window):
    screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
    x = (screen_geometry.width() - window.width()) / 2
    y = (screen_geometry.height() - window.height()) / 2
    window.move(int(x), int(y))

# Function to create a help pop up window
def help_pop_up():
    pop_up = QtWidgets.QWidget(win, QtCore.Qt.Window)
    pop_up.setWindowTitle("Help")
    pop_up.resize(400, 300)
    pop_up.setStyleSheet("background-color: white;")

    # Create a layout for the pop up window
    pop_up_layout = QtWidgets.QVBoxLayout(pop_up)

    # Create a label for 'For Help:' in big font
    help_label = QtWidgets.QLabel("For Help:")
    font = help_label.font()
    font.setPointSize(20)
    help_label.setFont(font)
    help_label.setAlignment(QtCore.Qt.AlignCenter)

    # Create a label for 'Contact us' in smaller font
    contact_label = QtWidgets.QLabel("Contact us at https://eigensensor.webflow.io/contact")
    font = contact_label.font()
    font.setPointSize(12)
    contact_label.setFont(font)
    contact_label.setAlignment(QtCore.Qt.AlignCenter)

    # Add the labels to the layout
    pop_up_layout.addWidget(help_label)
    pop_up_layout.addWidget(contact_label)

    # Center the pop up window
    center_window(pop_up)

    # Show the pop up window
    pop_up.show()

    # Create a cancel button
    cancel_button = QtWidgets.QPushButton("Cancel", pop_up)
    cancel_button.setGeometry(pop_up.width() - 50, 10, 40, 20)
    cancel_button.clicked.connect(pop_up.close)

    # Center the pop up window
    center_window(pop_up)

    # Show the pop up window
    pop_up.show()

# Add a navigation bar with buttons
def create_nav_bar():
    global isBandPass, isBandStop, notch

    nav_bar_widget = QWidget()
    nav_bar = QHBoxLayout()
    nav_bar_widget.setLayout(nav_bar)
    nav_bar_widget.setStyleSheet("background-color: #3B3838;")

    # Creating icons for the navigation bar
    # Add help icon to navigation bar
    help_button = create_nav_button("./images/help.png", 50, 50)
    # Add hamburger menu icon to navigation bar
    hamburger_button = create_nav_button("./images/hamburger.png", 50, 50)
    # Add logo to navigation bar
    logo_label = create_logo_label("./images/Logo-Dark.png", 80, 80)
    # Add setting icon to navigation bar
    settings_button = create_nav_button("./images/settings.png", 50, 50)

    # Adding icons to the navigation bar
    nav_bar.addWidget(hamburger_button)
    nav_bar.addWidget(logo_label)
    nav_bar.addStretch(1)
    nav_bar.addWidget(settings_button)
    nav_bar.addWidget(help_button)
    layout.addWidget(nav_bar_widget)

    # Function to update the settings; call the settings pop up window defined in the settings.py file and import the variables from that file, to be used in backend if needed
    def update_settings(win):
        global isBandPass, isBandStop
        from settings import settings_pop_up
        param1 = isBandPass
        param2 = isBandStop
        param3 = notch
        isBandPass, isBandStop = settings_pop_up(win, param1, param2, param3)

    # Connect the buttons to their respective functions
    hamburger_button.clicked.connect(toggle_menubar)
    help_button.clicked.connect(help_pop_up)
    # when settings button is clicked, i want to open up another window for settings
    settings_button.clicked.connect(lambda: update_settings(win))

    # Import the signals from the settings.py file
    from settings import settings_signals
    # Connect the signals from the settings window to the global variables
    settings_signals.bandPassChanged.connect(lambda state: globals().update({'isBandPass': state}))
    settings_signals.bandStopChanged.connect(lambda state: globals().update({'isBandStop': state}))
    settings_signals.notchChanged.connect(lambda state: globals().update({'notch': state}))


# Function to create a navigation button
def create_nav_button(icon_path, width, height):
    button = QPushButton()
    icon = QtGui.QIcon(icon_path)
    button.setIcon(icon)
    button.setIconSize(QtCore.QSize(width, height))
    button.setStyleSheet("border: none;")  # Remove button border
    return button

# Function to create a logo label
def create_logo_label(logo_path, width, height):
    logo_label = QLabel()
    logo_pixmap = QtGui.QPixmap(logo_path)
    logo_label.setPixmap(logo_pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio))
    return logo_label

# Add the navigation bar to the layout
create_nav_bar()

# Function to add a menubar to the layout
def add_menubar():
    global screen

    # Create a menubar widget
    menubar = QDockWidget("Navigate Screens", win)
    menubar.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
    # Create buttons for screen navigation
    time_series_button = QPushButton("Time Series")
    time_series_button.setStyleSheet("background-color: transparent; text-align: left;")
    fft_plot_button = QPushButton("FFT Plot")
    fft_plot_button.setStyleSheet("background-color: transparent; text-align: left;")
    classification_button = QPushButton("Classification")
    classification_button.setStyleSheet("background-color: transparent; text-align: left;")

    # Create layout for menubar content
    menubar_layout = QVBoxLayout()
    menubar_layout.addWidget(time_series_button)
    menubar_layout.addWidget(fft_plot_button)
    menubar_layout.addWidget(classification_button)

    def set_screen1():
        global screen
        screen = 1

    def set_screen2():
        global screen
        screen = 2

    def set_screen3():
        global screen
        screen = 3

    # Connect the buttons to their respective functions above
    time_series_button.clicked.connect(set_screen1)
    fft_plot_button.clicked.connect(set_screen2)
    classification_button.clicked.connect(set_screen3)

    # Add stretch to push widgets up
    menubar_layout.addStretch()

    # Set the menubar content layout
    menubar_content = QWidget()
    menubar_content.setLayout(menubar_layout)
    menubar.setWidget(menubar_content)
    win.addDockWidget(QtCore.Qt.LeftDockWidgetArea, menubar)
    menubar.hide()
    return menubar

# Add the menubar to the layout
menubar = add_menubar()

# Function to toggle the sidebar
def toggle_sidebar():
    if sidebar.isVisible():
        sidebar.hide()
    else:
        sidebar.show()

# Function to create a header which is below the navigation bar, unique to each window
def create_header():
    global isLossOfData

    # Create a header widget
    header_widget = QWidget()
    header = QHBoxLayout()
    header_widget.setLayout(header)
    header_widget.setStyleSheet("background-color: white;")

    sidebar_button = create_nav_button("./images/hamburger.png", 50, 50)
    header.addWidget(sidebar_button)
    
    # Add some space between the sidebar_button and the label
    spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    header.addItem(spacer)
    
    # Add the label to the header
    label = QLabel("Classification")
    font = label.font()
    font.setPointSize(20)
    label.setFont(font)
    header.addWidget(label)

    # Add some space between the label and the warning icon
    header.addStretch(1)

    header.addItem(spacer)
    header.addItem(spacer)

    # Add warning icon for loss of data [this conditional is to be changed later and updated in backend_classification.py]
    if isLossOfData:
        warning_icon = create_logo_label("./images/warning_bright.png", 80, 80)
        header.addWidget(warning_icon)
    else:
        warning_icon = create_logo_label("./images/warning_grey.png", 80, 80)
        header.addWidget(warning_icon)

    # # Add play button ONLY FOR PLAYBACK VERSION [THIS IS THE LIVE VERSION]
    # play_button = create_nav_button("./images/play.png", 50, 50)
    # header.addWidget(play_button)

    layout.addWidget(header_widget)

    sidebar_button.clicked.connect(toggle_sidebar)

# Add the header to the layout
create_header()

# Function to add a sidebar to the layout [screen settings]
def add_sidebar():
    # Sidebar widget
    sidebar = QDockWidget("Classification Options", win)
    sidebar.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

    # SSVEG VS EMG #
    # Create buttons for choosing between SSVEP and EMG
    ssvep = QPushButton("SSVEP")
    emg = QPushButton("EMG")

    # Set the buttons to be checkable
    ssvep.setCheckable(True)
    emg.setCheckable(True)

    # Set initial styles
    ssvep.setChecked(True)
    if ssvep.isChecked():
        ssvep.setStyleSheet("background-color: white;")
        emg.setStyleSheet("background-color: grey;")
    else:
        emg.setStyleSheet("background-color: white;")
        ssvep.setStyleSheet("background-color: grey;")

    # Group buttons together
    group = QButtonGroup()
    group.addButton(ssvep)
    group.addButton(emg)

    # Create layout for the buttons
    toggle_layout = QHBoxLayout()
    toggle_layout.addWidget(ssvep)
    toggle_layout.addWidget(emg) 
    
    # Function to change the style of the buttons when clicked
    def ssvep_clicked():
        ssvep.setStyleSheet("background-color: white;")
        emg.setStyleSheet("background-color: grey;")
        ssvep.setChecked(True)
        emg.setChecked(False)
    def emg_clicked():
        emg.setStyleSheet("background-color: white;")
        ssvep.setStyleSheet("background-color: grey;")
        emg.setChecked(True)
        ssvep.setChecked(False)

    # Connect the buttons to their respective functions
    ssvep.clicked.connect(ssvep_clicked)
    emg.clicked.connect(emg_clicked)

    # Add the layout to the sidebar layout
    sidebar_layout = QVBoxLayout()
    sidebar_layout.addLayout(toggle_layout)

    # Model Dropdown #
    # Create a label for the model dropdown
    model = QLabel("<b>Model</b>")
    sidebar_layout.addWidget(model)

    # Add the layout to the sidebar layout
    model_dropdown = QtWidgets.QComboBox()
    model_dropdown.addItem("1")
    model_dropdown.addItem("2")
    model_dropdown.addItem("3")

    sidebar_layout.addWidget(model_dropdown)

    # Function to change the model when the dropdown is changed
    def model_smooth():
        global model
        model = float(model_dropdown.currentText())

    # Connect the dropdown to the function
    model_dropdown.currentIndexChanged.connect(model_smooth)

    # Output Control Dropdown #
    # Create a label for the output control dropdown
    control = QLabel("<b>Output Control</b>")
    sidebar_layout.addWidget(control)

    # Add the layout to the sidebar layout
    control_dropdown = QtWidgets.QComboBox()
    control_dropdown.addItem("Spotify")
    control_dropdown.addItem("Robot")
    control_dropdown.addItem("etc")

    sidebar_layout.addWidget(control_dropdown)

    # Function to change the output control when the dropdown is changed
    def model_control():
        global output_control, isChanged
        output_control = control_dropdown.currentText()
        isChanged = True

    # Connect the dropdown to the function
    control_dropdown.currentIndexChanged.connect(model_control)

    # Push the widgets up within the sidebar
    sidebar_layout.addStretch()

    # Set the sidebar content layout
    sidebar_content = QWidget()
    sidebar_content.setLayout(sidebar_layout)
    sidebar.setWidget(sidebar_content)
    win.addDockWidget(QtCore.Qt.LeftDockWidgetArea, sidebar)
    sidebar.hide()
    return sidebar

# Add the sidebar to the layout
sidebar = add_sidebar()

# Create classification circles, all greyed out at the start [imported images]
circle1 = QLabel("")
pixmap = QPixmap('./images/greyed.png')
circle1.setPixmap(pixmap.scaled(50, 50))

circle2 = QLabel("")
pixmap = QPixmap('./images/greyed.png')
circle2.setPixmap(pixmap.scaled(50, 50))

circle3 = QLabel("")
pixmap = QPixmap('./images/greyed.png')
circle3.setPixmap(pixmap.scaled(50, 50))

circle4 = QLabel("")
pixmap = QPixmap('./images/greyed.png')
circle4.setPixmap(pixmap.scaled(50, 50))

# Function to update the classification bars and circles
def create_class(data_loaded_classification, classification_circle):
    global output_control, control1, control2, control3, control4, isCircle1, isCircle2, isCircle3, isCircle4, circle1, circle2, circle3, circle4

    spotify_options = ["Next Track", "Previous Track", "Play", "Pause", "Volume Up", "Volume Down"]

    # Create the header for all
    four_classes = QLabel("<b>4 Classes:</b>")
    font = four_classes.font()
    font.setPointSize(15)
    four_classes.setFont(font)
    four_classes.setAlignment(QtCore.Qt.AlignLeft)
    layout.addWidget(four_classes)

    class_layout = QHBoxLayout()

    # CLASS 1 #
    # Create the header for each individual class
    class1_layout = QVBoxLayout()
    class1_label = QLabel("<b>1: 6 Hz Stimuli</b>")
    font = class1_label.font()
    font.setPointSize(12)
    class1_label.setFont(font)
    class1_layout.addWidget(class1_label)
    # Create the layout for the circle and bar
    graph1_layout = QHBoxLayout()
    graph1_layout.setContentsMargins(0, 0, 0, 0)
    graph1_layout.setSpacing(0)
    graph1_layout.setAlignment(QtCore.Qt.AlignCenter)
    # Add the circle to the layout
    graph1_layout.addWidget(circle1)
    # Add the progress bar to the layout
    bar1 = QtWidgets.QProgressBar()
    bar1.setOrientation(QtCore.Qt.Vertical)
    bar1.setRange(0, 100)
    bar1.setValue(int(data_loaded_classification[0][0]))
    bar1.setStyleSheet("QProgressBar::chunk { background-color: #FFD966; }")
    bar1.setTextVisible(False)
    graph1_layout.addWidget(bar1)
    class1_layout.addLayout(graph1_layout)
    # Create the output control label at the bottom
    output_label1 = QLabel("<b>Output Control</b>")
    font = output_label1.font()
    font.setPointSize(10)
    output_label1.setFont(font)
    class1_layout.addWidget(output_label1)
    # Create the dropdown for the output control
    control1_dropdown = QtWidgets.QComboBox()
    for option in spotify_options:
        control1_dropdown.addItem(option)
    class1_layout.addWidget(control1_dropdown)
    # Function to change the output control when the dropdown is changed
    def model_control1():
        global control1
        control1 = control1_dropdown.currentText()
    # Connect the dropdown to the function
    control1_dropdown.currentIndexChanged.connect(model_control1)

    # CLASS 2 #
    class2_layout = QVBoxLayout()
    class2_label = QLabel("<b>2: 8 Hz Stimuli</b>")
    font = class2_label.font()
    font.setPointSize(12)
    class2_label.setFont(font)
    class2_layout.addWidget(class2_label)
    graph2_layout = QHBoxLayout()
    graph2_layout.setContentsMargins(0, 0, 0, 0)
    graph2_layout.setSpacing(0)
    graph2_layout.setAlignment(QtCore.Qt.AlignCenter)
    graph2_layout.addWidget(circle2)
    bar2 = QtWidgets.QProgressBar()
    bar2.setOrientation(QtCore.Qt.Vertical)
    bar2.setRange(0, 100)
    bar2.setValue(int(data_loaded_classification[1][0]))
    bar2.setStyleSheet("QProgressBar::chunk { background-color: #FFD966; }")
    bar2.setTextVisible(False)
    graph2_layout.addWidget(bar2)
    class2_layout.addLayout(graph2_layout)
    output_label2 = QLabel("<b>Output Control</b>")
    font = output_label2.font()
    font.setPointSize(10)
    output_label2.setFont(font)
    class2_layout.addWidget(output_label2)
    control2_dropdown = QtWidgets.QComboBox()
    for option in spotify_options:
        control2_dropdown.addItem(option)
    class2_layout.addWidget(control2_dropdown)
    def model_control2():
        global control2
        control2 = control2_dropdown.currentText()
    control2_dropdown.currentIndexChanged.connect(model_control2)

    # CLASS 3 #
    class3_layout = QVBoxLayout()
    class3_label = QLabel("<b>3: 10 Hz Stimuli</b>")
    font = class3_label.font()
    font.setPointSize(12)
    class3_label.setFont(font)
    class3_layout.addWidget(class3_label)
    graph3_layout = QHBoxLayout()
    graph3_layout.setContentsMargins(0, 0, 0, 0)
    graph3_layout.setSpacing(0)
    graph3_layout.setAlignment(QtCore.Qt.AlignCenter)
    graph3_layout.addWidget(circle3)
    bar3 = QtWidgets.QProgressBar()
    bar3.setOrientation(QtCore.Qt.Vertical)
    bar3.setRange(0, 100)
    bar3.setValue(int(data_loaded_classification[2][0]))
    bar3.setStyleSheet("QProgressBar::chunk { background-color: #FFD966; }")
    bar3.setTextVisible(False)
    graph3_layout.addWidget(bar3)
    class3_layout.addLayout(graph3_layout)
    output_label3 = QLabel("<b>Output Control</b>")
    font = output_label3.font()
    font.setPointSize(10)
    output_label3.setFont(font)
    class3_layout.addWidget(output_label3)
    control3_dropdown = QtWidgets.QComboBox()
    for option in spotify_options:
        control3_dropdown.addItem(option)
    class3_layout.addWidget(control3_dropdown)
    def model_control3():
        global control3
        control3 = control3_dropdown.currentText()
    control3_dropdown.currentIndexChanged.connect(model_control3)

    # CLASS 4 #
    class4_layout = QVBoxLayout()
    class4_label = QLabel("<b>4: 12 Hz Stimuli</b>")
    font = class4_label.font()
    font.setPointSize(12)
    class4_label.setFont(font)
    class4_layout.addWidget(class4_label)
    graph4_layout = QHBoxLayout()
    graph4_layout.setContentsMargins(0, 0, 0, 0)
    graph4_layout.setSpacing(0)
    graph4_layout.setAlignment(QtCore.Qt.AlignCenter)
    graph4_layout.addWidget(circle4)
    bar4 = QtWidgets.QProgressBar()
    bar4.setOrientation(QtCore.Qt.Vertical)
    bar4.setRange(0, 100)
    bar4.setValue(int(data_loaded_classification[3][0]))
    bar4.setStyleSheet("QProgressBar::chunk { background-color: #FFD966; }")
    bar4.setTextVisible(False)
    graph4_layout.addWidget(bar4)
    class4_layout.addLayout(graph4_layout)
    output_label4 = QLabel("<b>Output Control</b>")
    font = output_label4.font()
    font.setPointSize(10)
    output_label4.setFont(font)
    class4_layout.addWidget(output_label4)
    control4_dropdown = QtWidgets.QComboBox()
    for option in spotify_options:
        control4_dropdown.addItem(option)
    class4_layout.addWidget(control4_dropdown)
    def model_control4():
        global control4
        control4 = control4_dropdown.currentText()
    control4_dropdown.currentIndexChanged.connect(model_control4)

    class_layout.addLayout(class1_layout)
    class_layout.addLayout(class2_layout)
    class_layout.addLayout(class3_layout)
    class_layout.addLayout(class4_layout)

    layout.addLayout(class_layout)

    return bar1, bar2, bar3, bar4, control1_dropdown, control2_dropdown, control3_dropdown, control4_dropdown

# Randomise and populate the dataset
data_loaded_classification = np.random.rand(4,1)
data_loaded_classification = data_loaded_classification * 100 # make it out of 100 instead of 1
classification_circle = np.zeros(4)
classification_circle[data_loaded_classification.argmax()] = 1

bar1, bar2, bar3, bar4, control1_dropdown, control2_dropdown, control3_dropdown, control4_dropdown = create_class(data_loaded_classification, classification_circle)
