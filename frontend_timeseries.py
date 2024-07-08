import numpy as np
import os
import datetime
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QLabel, QDockWidget, QLineEdit
from PyQt5.QtWidgets import QRadioButton, QButtonGroup

# Initialization
min_freq = -100
max_freq = 100
refresh_interval_ms = 100
curves = []
plots = []
isLossOfData = False
time_lapsed = 10
rates = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
screen = 1
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

# Create a function to toggle the visibility of the menubar
def toggle_menubar():
    if menubar.isVisible():
        menubar.hide()
    else:
        menubar.show()

# Center the window
def center_window(window):
    screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
    x = (screen_geometry.width() - window.width()) / 2
    y = (screen_geometry.height() - window.height()) / 2
    window.move(int(x), int(y))

# Create a help pop up window
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
    settings_button.clicked.connect(lambda: update_settings(win))

    from settings import settings_signals
    # Connect the signals from the settings window to the global variables
    settings_signals.bandPassChanged.connect(lambda state: globals().update({'isBandPass': state}))
    settings_signals.bandStopChanged.connect(lambda state: globals().update({'isBandStop': state}))
    settings_signals.notchChanged.connect(lambda state: globals().update({'notch': state}))

# Create a navigation button
def create_nav_button(icon_path, width, height):
    button = QPushButton()
    icon = QtGui.QIcon(icon_path)
    button.setIcon(icon)
    button.setIconSize(QtCore.QSize(width, height))
    button.setStyleSheet("border: none;")  # Remove button border
    return button

# Create a logo label
def create_logo_label(logo_path, width, height):
    logo_label = QLabel()
    logo_pixmap = QtGui.QPixmap(logo_path)
    logo_label.setPixmap(logo_pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio))
    return logo_label

# Add a navigation bar
create_nav_bar()

# Function to add a menubar
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

# Add the menubar
menubar = add_menubar()

# Function to toggle the visibility of the sidebar
def toggle_sidebar():
    if sidebar.isVisible():
        sidebar.hide()
    else:
        sidebar.show()

# Create a header
def create_header():
    global isLossOfData

    header_widget = QWidget()
    header = QHBoxLayout()
    header_widget.setLayout(header)
    header_widget.setStyleSheet("background-color: white;")

    # Add a sidebar button
    sidebar_button = create_nav_button("./images/hamburger.png", 50, 50)
    header.addWidget(sidebar_button)
    
    # Add some space between the sidebar_button and the label
    spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    header.addItem(spacer)
    
    # Add a label for the time series
    time_series_label = QLabel("Time Series")
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

    # Add warning icon for loss of data with a conditional statement
    if isLossOfData:
        warning_icon = create_logo_label("./images/warning_bright.png", 80, 80)
        header.addWidget(warning_icon)
    else:
        warning_icon = create_logo_label("./images/warning_grey.png", 80, 80)
        header.addWidget(warning_icon)

    # # Add play button FOR PLAYBACK VERSION
    # play_button = create_nav_button("./images/play.png", 50, 50)
    # header.addWidget(play_button)

    # Create a layout for the side buttons for each plotted graph below the header
    def set_up_buttons(rates=[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]):
        rates_label =[]
        buttons_layout = QVBoxLayout()
        # Add buttons for graph selection with its paired rates (right now is static but can be updated based on stream data in backend)
        colors = ['#FF0000', '#0404C9', '#008000', '#800080', '#FFC0CB', '#FFFF00', '#000000', '#00FFFF']
        graph_buttons = []
        for i in range(8):
            button = QPushButton(f"{i+1}")
            button.setStyleSheet(f"border: 2px solid {colors[i]};")
            button.setFixedWidth(40)
            graph_buttons.append(button)
            rate = QLabel(str(rates[i]) + " uVrms")
            rates_label.append(rate)
            
            pair_layout = QVBoxLayout()
            pair_layout.addWidget(button)
            pair_layout.addWidget(rate)
            buttons_layout.addLayout(pair_layout)

            spacer = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            buttons_layout.addItem(spacer)

            # If button was clicked, toggle the visibility of the graph and everything else for the respective index
            button.clicked.connect(lambda checked, index=i: toggle_graph(index))

        return buttons_layout, rates_label, graph_buttons
    
    buttons_below, rates_label, graph = set_up_buttons()

    # Function to toggle the visibility of a graph
    def toggle_graph(index):
        if plots[index].isVisible():
            plots[index].setVisible(False)
            graph_buttons[index].setStyleSheet("border: none;")

            # Settings visibility of the side labels of each graph
            rates_label[index].setVisible(False)
            graph[index].setVisible(False)
        else:
            plots[index].setVisible(True)
            graph_buttons[index].setStyleSheet(f"border: 2px solid {colors[index]};")

            # Settings visibility of the side labels of each graph
            rates_label[index].setVisible(True)
            graph[index].setVisible(True)

        # Filter and get a list of visible plots
        visible_plots = [plot for plot in plots if plot.isVisible()]

        # Hide the x axis of all the plots except the last visible plot
        for i, plot in enumerate(visible_plots[:-1]):
            plot.getAxis('bottom').setStyle(showValues=False)
            plot.getAxis('bottom').setVisible(False)

        # Set the x axis of the last visible plot to be visible
        visible_plots[-1].getAxis('bottom').setStyle(showValues=True)
        visible_plots[-1].getAxis('bottom').setVisible(True)

    layout.addWidget(header_widget)

    sidebar_button.clicked.connect(toggle_sidebar)

    return buttons_below, rates_label

# Add the header
buttons_layout, rates_label = create_header() # in the backend import rates_label and update it during stream based on how rates[] changes

# Function to add a sidebar
def add_sidebar():
    # Sidebar widget
    sidebar = QDockWidget("Time Series Options", win)
    sidebar.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

    # Create input fields for min_freq and max_freq
    amp = QLabel("<b>Amplitude (uV)</b>")
    min_freq_label = QLabel("Minimum")
    min_freq_input = QLineEdit(str(min_freq))
    max_freq_label = QLabel("Maximum")
    max_freq_input = QLineEdit(str(max_freq))

    # Create layout for labels and inputs
    label_layout = QHBoxLayout()
    label_layout.addWidget(min_freq_label)
    label_layout.addWidget(max_freq_label)

    input_layout = QHBoxLayout()
    input_layout.addWidget(min_freq_input)
    input_layout.addWidget(max_freq_input)

    # Add the layout to the sidebar layout
    time = QLabel("<b>Time Lapsed (s)</b>")
    time_input = QLineEdit(str(time_lapsed))
    time_layout = QHBoxLayout()
    time_layout.addWidget(time)
    time_layout.addWidget(time_input)

    # Create radio buttons for time option selection
    time_option_label = QLabel("<b>Time</b>")

    relative = QPushButton("Relative")
    absolute = QPushButton("Absolute")

    relative.setCheckable(True)
    absolute.setCheckable(True)

    # Set initial styles
    relative.setChecked(True)
    if relative.isChecked():
        relative.setStyleSheet("background-color: white;")
        absolute.setStyleSheet("background-color: grey;")
    else:
        absolute.setStyleSheet("background-color: white;")
        relative.setStyleSheet("background-color: grey;")

    # Group buttons together
    time_option_group = QButtonGroup()
    time_option_group.addButton(relative)
    time_option_group.addButton(absolute)

    # Create layout for radio buttons
    toggle_layout = QHBoxLayout()
    toggle_layout.addWidget(relative)
    toggle_layout.addWidget(absolute) 
    
    # Function to toggle the time option
    def relative_clicked():
        relative.setStyleSheet("background-color: white;")
        absolute.setStyleSheet("background-color: grey;")
        relative.setChecked(True)
        absolute.setChecked(False)
        print("Relative time option selected")
    def absolute_clicked():
        absolute.setStyleSheet("background-color: white;")
        relative.setStyleSheet("background-color: grey;")
        absolute.setChecked(True)
        relative.setChecked(False)
        print("Absolute time option selected")

    # Connect the toggle_time_option function to the toggle button
    relative.clicked.connect(relative_clicked)
    absolute.clicked.connect(absolute_clicked)

    # Create layout for sidebar content
    sidebar_layout = QVBoxLayout()
    sidebar_layout.addWidget(amp)
    sidebar_layout.addLayout(label_layout)
    sidebar_layout.addLayout(input_layout)
    sidebar_layout.addLayout(time_layout)
    sidebar_layout.addWidget(time_option_label)
    sidebar_layout.addLayout(toggle_layout)

    # Update min_freq and max_freq when input fields are changed
    def update_freq():
        global min_freq, max_freq
        min_freq = float(min_freq_input.text())
        max_freq = float(max_freq_input.text())

    # Update time_lapsed when input field is changed
    def update_time():
        global time_lapsed
        time_lapsed = float(time_input.text())

    # Connect the input fields to their respective functions
    min_freq_input.textChanged.connect(update_freq)
    max_freq_input.textChanged.connect(update_freq)
    time_input.textChanged.connect(update_time)

    # Add stretch to push widgets up
    sidebar_layout.addStretch()

    # Set the sidebar content layout
    sidebar_content = QWidget()
    sidebar_content.setLayout(sidebar_layout)
    sidebar.setWidget(sidebar_content)
    win.addDockWidget(QtCore.Qt.LeftDockWidgetArea, sidebar)
    sidebar.hide()
    return sidebar

# Add the sidebar
sidebar = add_sidebar()

# Add the graph layout
graph_layout = QHBoxLayout()
plot_widget = pg.GraphicsLayoutWidget()
plot_widget.setBackground('w')
# Use the buttons_layout defined under create_header() to add the buttons to the sidebar
graph_layout.addLayout(buttons_layout)
graph_layout.addWidget(plot_widget)
layout.addLayout(graph_layout)

# Initialize the plot
def initialize_plot(data, min_freq=min_freq, max_freq=max_freq, time_lapsed=time_lapsed):
    global curves, plots

    # Create plots with respective colours for each plotted curve
    colors = ['#FF0000', '#0404C9', '#008000', '#800080', '#FFC0CB', '#FFFF00', '#000000', '#00FFFF']

    for i in range(8):
        p = plot_widget.addPlot()
        p.setYRange(min_freq, max_freq)
        p.setXRange(0, time_lapsed)
        p.showGrid(x=False, y=True, alpha=0.3)  # Set as false for x axis because will have difference for relative and absolute, can change later
        plots.append(p)
        curves.append(p.plot(data[0], data[i+1], pen=pg.mkPen(colors[i], width=2)))
        plot_widget.nextRow()

    # Filter and get a list of visible plots
    visible_plots = [plot for plot in plots if plot.isVisible()]

    # Hide the x axis of all the plots except the last visible plot
    for i, plot in enumerate(visible_plots[:-1]):
        plot.getAxis('bottom').setStyle(showValues=False)
        plot.getAxis('bottom').setVisible(False)

    return plots, curves
