import numpy as np
import os
import datetime
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QLabel, QDockWidget, QLineEdit
from PyQt5.QtWidgets import QRadioButton, QButtonGroup

# Initialization
min_freq = 0
max_freq = 60
min_amp = 0.1
max_amp = 100
smooth = 0.9
refresh_interval_ms = 100
curves = []
plots = []
isLossOfData = False
isFiltered = True
screen = 2
isBandPass = True
isBandStop = False
notch = '50'

# Create the application
app = QtWidgets.QApplication([])
win = QtWidgets.QMainWindow()
win.setWindowTitle("EigenSensor")
win.resize(1000, 1000)

central_widget = QWidget()
layout = QVBoxLayout()
central_widget.setLayout(layout)
win.setCentralWidget(central_widget)

# Function to toggle the visibility of the menubar
def toggle_menubar():
    if menubar.isVisible():
        menubar.hide()
    else:
        menubar.show()

# Function to center the window
def center_window(window):
    screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
    x = (screen_geometry.width() - window.width()) / 2
    y = (screen_geometry.height() - window.height()) / 2
    window.move(int(x), int(y))

# Function to create a help pop up window
def help_pop_up():
    # Create a pop up window
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

    # Create navigation bar buttons
    # Add help icon to navigation bar
    help_button = create_nav_button("./images/help.png", 50, 50)
    # Add hamburger menu icon to navigation bar
    hamburger_button = create_nav_button("./images/hamburger.png", 50, 50)
    # Add logo to navigation bar
    logo_label = create_logo_label("./images/Logo-Dark.png", 80, 80)
    # Add setting icon to navigation bar
    settings_button = create_nav_button("./images/settings.png", 50, 50)

    # Add the buttons to the navigation bar layout
    nav_bar.addWidget(hamburger_button)
    nav_bar.addWidget(logo_label)
    nav_bar.addStretch(1)
    nav_bar.addWidget(settings_button)
    nav_bar.addWidget(help_button)
    layout.addWidget(nav_bar_widget)

    # Function to update the settings
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

    # Connect the signals from the settings window to the global variables
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

# Add a navigation bar to the window
create_nav_bar()

# Function to add a menubar to the window
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

# Add the menubar to the window
menubar = add_menubar()

# Function to toggle the visibility of the sidebar
def toggle_sidebar():
    if sidebar.isVisible():
        sidebar.hide()
    else:
        sidebar.show()

# Function to create a header
def create_header():
    global isLossOfData

    header_widget = QWidget()
    header = QHBoxLayout()
    header_widget.setLayout(header)
    header_widget.setStyleSheet("background-color: white;")

    # Add a sidebar settings button to the header
    sidebar_button = create_nav_button("./images/hamburger.png", 50, 50)
    header.addWidget(sidebar_button)
    
    # Add some space between the sidebar_button and the label
    spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    header.addItem(spacer)
    
    # Add a label for the header
    time_series_label = QLabel("FFT Plot")
    font = time_series_label.font()
    font.setPointSize(20)
    time_series_label.setFont(font)
    header.addWidget(time_series_label)

    # Add some space between the label and the buttons
    header.addStretch(1)

    # Add buttons for graph selection
    colors = ['#FF0000', '#0404C9', '#008000', '#800080', '#FFC0CB', '#FFFF00', '#000000', '#00FFFF']
    graph_buttons = []
    for i in range(8):
        button = QPushButton(f"{i+1}")
        button.setStyleSheet(f"border: 2px solid {colors[i]};")
        button.setFixedWidth(40)  # Set the width of each button to 20
        graph_buttons.append(button)
        header.addWidget(button)
        button.clicked.connect(lambda checked, index=i: toggle_graph(index))

    # Add some space between the buttons and the warning icon
    header.addItem(spacer)
    header.addItem(spacer)

    # Add warning icon for loss of data with a conditional
    if isLossOfData:
        warning_icon = create_logo_label("./images/warning_bright.png", 80, 80)
        header.addWidget(warning_icon)
    else:
        warning_icon = create_logo_label("./images/warning_grey.png", 80, 80)
        header.addWidget(warning_icon)

    # # Add play button FOR PLAYBACK VERSION
    # play_button = create_nav_button("./images/play.png", 50, 50)
    # header.addWidget(play_button)

    # Function to toggle the visibility of a graph based on clicking the buttons above
    def toggle_graph(index):
        if curves[index].isVisible():
            curves[index].setVisible(False)
            graph_buttons[index].setStyleSheet("border: none;")
        else:
            curves[index].setVisible(True)
            graph_buttons[index].setStyleSheet(f"border: 2px solid {colors[index]};")

    layout.addWidget(header_widget)

    sidebar_button.clicked.connect(toggle_sidebar)

# Add a header to the window
create_header()

# Function to add a sidebar to the window
def add_sidebar():
    # Sidebar widget
    sidebar = QDockWidget("FFT Plot Options", win)
    sidebar.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

    # Create input fields for max_freq
    freq = QLabel("<b>Frequency (Hz)</b>")
    max_freq_label = QLabel("Maximum")
    max_freq_input = QLineEdit(str(max_freq))

    # Create input fields for min_amp and max_amp
    amp = QLabel("<b>Amplitude (uV)</b>")
    min_amp_label = QLabel("Minimum")
    min_amp_input = QLineEdit(str(min_amp))
    max_amp_label = QLabel("Maximum")
    max_amp_input = QLineEdit(str(max_amp))

    # Create layout for labels and inputs
    label_layout = QHBoxLayout()
    label_layout.addWidget(min_amp_label)
    label_layout.addWidget(max_amp_label)

    input_layout = QHBoxLayout()
    input_layout.addWidget(min_amp_input)
    input_layout.addWidget(max_amp_input)

    # Add the smooth dropdown to the sidebar layout
    smooth = QLabel("<b>Smooth</b>")
    smooth_dropdown = QtWidgets.QComboBox()
    smooth_dropdown.addItem("0.0")
    smooth_dropdown.addItem("0.5")
    smooth_dropdown.addItem("0.75")
    smooth_dropdown.addItem("0.9")
    smooth_dropdown.addItem("0.95")
    smooth_dropdown.addItem("0.98")
    smooth_dropdown.addItem("0.99")
    smooth_dropdown.addItem("0.999")
    smooth_layout = QHBoxLayout()
    smooth_layout.addWidget(smooth)
    smooth_layout.addWidget(smooth_dropdown)

    # Function to update the smooth value
    def update_smooth():
        global smooth
        smooth = float(smooth_dropdown.currentText())

    # Connect the smooth dropdown to the update_smooth function
    smooth_dropdown.currentIndexChanged.connect(update_smooth)

    # Add the filter button to the sidebar layout
    def toggle_filter():
        global isFiltered
        if filter_button.text() == " ":
            isFiltered = True
            filter_button.setText("X")
        else:
            isFiltered = False
            filter_button.setText(" ")
    filter_layout = QHBoxLayout()
    filter_button = QPushButton("X")
    filter_button.setFixedWidth(40)
    filter_layout.addWidget(filter_button)
    filter_button.clicked.connect(toggle_filter)
    filter_label = QLabel("Filtered")
    filter_layout.addWidget(filter_label)
    filter_layout.addStretch(1)

    # Create radio buttons for regression option selection
    log = QPushButton("Log")
    lin = QPushButton("Lin")

    # Set radio buttons to checkable
    log.setCheckable(True)
    lin.setCheckable(True)

    # Set initial styles
    log.setChecked(True)
    if log.isChecked():
        log.setStyleSheet("background-color: white;")
        lin.setStyleSheet("background-color: grey;")
    else:
        lin.setStyleSheet("background-color: white;")
        log.setStyleSheet("background-color: grey;")

    # Group buttons together
    group = QButtonGroup()
    group.addButton(log)
    group.addButton(lin)

    # Create layout for radio buttons
    toggle_layout = QHBoxLayout()
    toggle_layout.addWidget(log)
    toggle_layout.addWidget(lin) 
    
    # Function to update the radio buttons
    def log_clicked():
        log.setStyleSheet("background-color: white;")
        lin.setStyleSheet("background-color: grey;")
        log.setChecked(True)
        lin.setChecked(False)
        print("Relative time option selected")
    def lin_clicked():
        lin.setStyleSheet("background-color: white;")
        log.setStyleSheet("background-color: grey;")
        lin.setChecked(True)
        log.setChecked(False)
        print("Absolute time option selected")

    # Connect the radio buttons to their respective functions
    log.clicked.connect(log_clicked)
    lin.clicked.connect(lin_clicked)

    # Create layout for sidebar content and add all components to the layout
    sidebar_layout = QVBoxLayout()
    sidebar_layout.addWidget(freq)
    sidebar_layout.addWidget(max_freq_label)
    sidebar_layout.addWidget(max_freq_input)
    sidebar_layout.addWidget(amp)
    sidebar_layout.addLayout(label_layout)
    sidebar_layout.addLayout(input_layout)
    sidebar_layout.addLayout(smooth_layout)
    sidebar_layout.addLayout(filter_layout)
    sidebar_layout.addLayout(toggle_layout)

    # Function to update the max_freq value
    def update_freq():
        global max_freq
        max_freq = float(max_freq_input.text())

    # Function to update the min_amp and max_amp values
    def update_amp():
        global min_amp, max_amp
        min_amp = float(min_amp_input.text())
        max_amp = float(max_amp_input.text())

    # Connect the input fields to their respective functions
    max_freq_input.textChanged.connect(update_freq)
    min_amp_input.textChanged.connect(update_amp)
    max_amp_input.textChanged.connect(update_amp)

    # Add stretch to push widgets up
    sidebar_layout.addStretch()

    # Set the sidebar content layout
    sidebar_content = QWidget()
    sidebar_content.setLayout(sidebar_layout)
    sidebar.setWidget(sidebar_content)
    win.addDockWidget(QtCore.Qt.LeftDockWidgetArea, sidebar)
    sidebar.hide()
    return sidebar

# Add the sidebar to the window
sidebar = add_sidebar()

# Function to create the plot widget
plot_widget = pg.GraphicsLayoutWidget()
plot_widget.setBackground('w')
layout.addWidget(plot_widget)

# Initialize the plot and the curves
def initialize_plot(data, min_freq=min_freq, max_freq=max_freq, min_amp=min_amp, max_amp=max_amp):
    global curves, plots

    # Define the different colors for the curves
    colors = ['#FF0000', '#0404C9', '#008000', '#800080', '#FFC0CB', '#FFFF00', '#000000', '#00FFFF']
    
    # Create a single plot
    p = plot_widget.addPlot()
    p.setXRange(min_freq, max_freq)
    p.setYRange(min_amp, max_amp)
    p.showGrid(x=True, y=True, alpha=0.3)  # Set as false for x axis because will have difference for relative and absolute, can change later
    p.setLabel('bottom', 'Frequency (Hz)')
    p.setLabel('left', 'Amplitude (uV)')

    # Overlay all curves on top of each other, with the final curve on top
    for i in range(8):
        curves.append(p.plot(data[0], data[i+1], pen=pg.mkPen(colors[i], width=2)))

    plots.append(p)

    return plots, curves
