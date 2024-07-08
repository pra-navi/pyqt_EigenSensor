from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QLabel, QDockWidget, QLineEdit
from PyQt5.QtWidgets import QRadioButton, QButtonGroup, QComboBox, QGraphicsPixmapItem
from PyQt5.QtCore import pyqtSignal, QObject

# Create a button with an icon
def create_nav_button(icon_path, width, height):
    button = QPushButton()
    icon = QtGui.QIcon(icon_path)
    button.setIcon(icon)
    button.setIconSize(QtCore.QSize(width, height))
    button.setStyleSheet("border: none;")  # Remove button border
    return button

# Center the window
def center_window(window):
    screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
    x = (screen_geometry.width() - window.width()) / 2
    y = (screen_geometry.height() - window.height()) / 2
    window.move(int(x), int(y))

# Settings signal to always update these variables and export it to the backend
class SettingsSignals(QObject):
    bandPassChanged = pyqtSignal(bool)
    bandStopChanged = pyqtSignal(bool)
    notchChanged = pyqtSignal(str)
settings_signals = SettingsSignals()

# Settings variables intialised

channel1_value = ""
channel2_value = ""
channel3_value = ""
channel4_value = ""
channel5_value = ""
channel6_value = ""
channel7_value = ""
channel8_value = ""

start0 = 5
start1 = 5
start2 = 5
start3 = 5
start4 = 5
start5 = 5
start6 = 5
start7 = 5
start8 = 5

stop0 = 50
stop1 = 50
stop2 = 50
stop3 = 50
stop4 = 50
stop5 = 50
stop6 = 50
stop7 = 50
stop8 = 50

type0 = "Butterworth"
type1 = "Butterworth"
type2 = "Butterworth"
type3 = "Butterworth"
type4 = "Butterworth"
type5 = "Butterworth"
type6 = "Butterworth"
type7 = "Butterworth"
type8 = "Butterworth"

order0 = 4
order1 = 4
order2 = 4
order3 = 4
order4 = 4
order5 = 4
order6 = 4
order7 = 4
order8 = 4

bias1 = "Yes"
bias2 = "Yes"
bias3 = "Yes"
bias4 = "Yes"
bias5 = "Yes"
bias6 = "Yes"
bias7 = "Yes"
bias8 = "Yes"

srb11 = "On"
srb12 = "On"
srb13 = "On"
srb14 = "On"
srb15 = "On"
srb16 = "On"
srb17 = "On"
srb18 = "On"

srb21 = "On"
srb22 = "On"
srb23 = "On"
srb24 = "On"
srb25 = "On"
srb26 = "On"
srb27 = "On"
srb28 = "On"

input1 = "Normal"
input2 = "Normal"
input3 = "Normal"
input4 = "Normal"
input5 = "Normal"
input6 = "Normal"
input7 = "Normal"
input8 = "Normal"

pga1 = 24
pga2 = 24
pga3 = 24
pga4 = 24
pga5 = 24
pga6 = 24
pga7 = 24
pga8 = 24

# Create a pop up window for settings
def settings_pop_up(win, isBandPass, isBandStop, notch):
    # Create a pop up window
    pop_up = QtWidgets.QWidget(win, QtCore.Qt.Window)
    pop_up.setWindowTitle("Settings")
    pop_up.resize(1000, 1000)
    pop_up.setStyleSheet("background-color: white;")
    pop_up_layout = QtWidgets.QVBoxLayout(pop_up)

    # Create a label for 'Settings' in big font
    back_button = create_nav_button("./images/back_button.png", 50, 50)
    back_button.clicked.connect(pop_up.close)
    heading = QHBoxLayout()
    heading.addWidget(back_button, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    settings_label = QtWidgets.QLabel("Settings")
    font = settings_label.font()
    font.setPointSize(20)
    settings_label.setFont(font)
    settings_label.setAlignment(QtCore.Qt.AlignLeft)
    heading.addWidget(settings_label)
    heading.addStretch(1)

    setting_layout = QHBoxLayout()

    buttons_layout = QVBoxLayout()
    buttons_layout.setAlignment(QtCore.Qt.AlignTop)

    # Create a stacked layout to switch between 'Software', 'Impedance Check' and 'Hardware'
    def set_software():
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QtGui.QColor(0, 0, 0, 160))
        shadow.setOffset(5, 5)
        software_button.setStyleSheet("background-color: #3B3838; color: white; text-align: center;")
        software_button.setGraphicsEffect(shadow)
        impedance_button.setStyleSheet("background-color: #FFD966; color: black; text-align: center;")
        impedance_button.setGraphicsEffect(None)
        hardware_button.setStyleSheet("background-color: #3B3838; color: white; text-align: center;")
        hardware_button.setGraphicsEffect(None)
        stacked_layout.setCurrentIndex(0)
    def set_impedance():
        software_button.setStyleSheet("background-color: #3B3838; color: white; text-align: center;")
        software_button.setGraphicsEffect(None)
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QtGui.QColor(0, 0, 0, 160))
        shadow.setOffset(5, 5)
        impedance_button.setStyleSheet("background-color: #FFD966; color: black; text-align: center;")
        impedance_button.setGraphicsEffect(shadow)
        hardware_button.setStyleSheet("background-color: #3B3838; color: white; text-align: center;")
        hardware_button.setGraphicsEffect(None)
        stacked_layout.setCurrentIndex(1)
    def set_hardware():
        software_button.setStyleSheet("background-color: #3B3838; color: white; text-align: center;")
        software_button.setGraphicsEffect(None)
        impedance_button.setStyleSheet("background-color: #FFD966; color: black; text-align: center;")
        impedance_button.setGraphicsEffect(None)
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QtGui.QColor(0, 0, 0, 160))
        shadow.setOffset(5, 5)
        hardware_button.setStyleSheet("background-color: #3B3838; color: white; text-align: center;")
        hardware_button.setGraphicsEffect(shadow)
        stacked_layout.setCurrentIndex(2)

    # Create a button for 'Software'
    software_button = QtWidgets.QPushButton("Software")
    software_button.setStyleSheet("background-color: #3B3838; color: white; text-align: center;")
    software_button.setFixedSize(200, 50)
    software_button.clicked.connect(set_software)

    # Create a button for 'Impedance Check'
    impedance_button = QtWidgets.QPushButton("Impedance Check")
    impedance_button.setStyleSheet("background-color: #FFD966; color: black; text-align: center;")
    impedance_button.setFixedSize(200, 50)
    impedance_button.clicked.connect(set_impedance)

    # Create a button for 'Hardware'
    hardware_button = QtWidgets.QPushButton("Hardware")
    hardware_button.setStyleSheet("background-color: #3B3838; color: white; text-align: center;")
    hardware_button.setFixedSize(200, 50)
    hardware_button.clicked.connect(set_hardware)

    buttons_layout.addWidget(software_button)
    buttons_layout.addWidget(impedance_button)
    buttons_layout.addWidget(hardware_button)
    buttons_layout.addStretch()

    # SOFTWARE LAYOUT #
    software_layout = QVBoxLayout()
    software_layout.setAlignment(QtCore.Qt.AlignTop)

    # Filter layout #
    # Create a label for 'Filter'
    filter_layout = QHBoxLayout()
    filter_label = QLabel("Filter: ")
    filter_layout.addWidget(filter_label)

    # Create two buttons for 'Band Pass' and 'Band Stop'
    bandpass = QPushButton("Band Pass")
    bandstop = QPushButton("Band Stop")

    bandpass.setCheckable(True)
    bandstop.setCheckable(True)

    # Set initial styles
    bandpass.setChecked(isBandPass)
    bandstop.setChecked(isBandStop)
    if bandpass.isChecked():
        bandpass.setStyleSheet("background-color: white;")
        bandstop.setStyleSheet("background-color: grey;")
    else:
        bandstop.setStyleSheet("background-color: white;")
        bandpass.setStyleSheet("background-color: grey;")

    # Group buttons together
    group = QButtonGroup()
    group.addButton(bandpass)
    group.addButton(bandstop)

    # Create a horizontal layout for the buttons
    toggle_layout = QHBoxLayout()
    toggle_layout.addWidget(bandpass)
    toggle_layout.addWidget(bandstop) 
    
    # Set the filter type when the buttons are clicked
    def bandpass_clicked():
        bandpass.setStyleSheet("background-color: white;")
        bandstop.setStyleSheet("background-color: grey;")
        bandpass.setChecked(True)
        isBandPass = True
        settings_signals.bandPassChanged.emit(True)
        bandstop.setChecked(False)
        isBandStop = False
        settings_signals.bandStopChanged.emit(False)
    def bandstop_clicked():
        bandstop.setStyleSheet("background-color: white;")
        bandpass.setStyleSheet("background-color: grey;")
        bandstop.setChecked(True)
        isBandStop = True
        settings_signals.bandStopChanged.emit(True)
        bandpass.setChecked(False)
        isBandPass = False
        settings_signals.bandPassChanged.emit(False)

    # Connect the buttons to the functions
    bandpass.clicked.connect(bandpass_clicked)
    bandstop.clicked.connect(bandstop_clicked)

    spacer = QWidget()
    spacer.setFixedWidth(20)
    filter_layout.addWidget(spacer)

    filter_layout.addLayout(toggle_layout)
    filter_layout.addStretch(1)
    software_layout.addLayout(filter_layout)

    # Notch layout #
    notch_layout = QHBoxLayout()
    notch_label = QLabel("Notch (Hz): ")
    notch_layout.addWidget(notch_label)
    notch50 = QPushButton("50")
    notch60 = QPushButton("60")
    notchAll = QPushButton("50 + 60")
    notchNone = QPushButton("None")
    notch50.setCheckable(True)
    notch60.setCheckable(True)
    notchAll.setCheckable(True)
    notchNone.setCheckable(True)
    notch50.setFixedSize(80, 40)
    notch60.setFixedSize(80, 40)
    notchAll.setFixedSize(80, 40)
    notchNone.setFixedSize(80, 40)

    # Set styles
    if notch == "50":
        notch50.setStyleSheet("background-color: #E0E0E0; color: black; border: 2px solid #FFD966;")
        notch60.setStyleSheet("background-color: #E0E0E0; color: black;")
        notchAll.setStyleSheet("background-color: #E0E0E0; color: black;")
        notchNone.setStyleSheet("background-color: #E0E0E0; color: black;")
    elif notch == "60":
        notch50.setStyleSheet("background-color: #E0E0E0; color: black;")
        notch60.setStyleSheet("background-color: #E0E0E0; color: black; border: 2px solid #FFD966;")
        notchAll.setStyleSheet("background-color: #E0E0E0; color: black;")
        notchNone.setStyleSheet("background-color: #E0E0E0; color: black;")
    elif notch == "50 + 60":
        notch50.setStyleSheet("background-color: #E0E0E0; color: black;")
        notch60.setStyleSheet("background-color: #E0E0E0; color: black;")
        notchAll.setStyleSheet("background-color: #E0E0E0; color: black; border: 2px solid #FFD966;")
        notchNone.setStyleSheet("background-color: #E0E0E0; color: black;")
    elif notch == "None":
        notch50.setStyleSheet("background-color: #E0E0E0; color: black;")
        notch60.setStyleSheet("background-color: #E0E0E0; color: black;")
        notchAll.setStyleSheet("background-color: #E0E0E0; color: black;")
        notchNone.setStyleSheet("background-color: #E0E0E0; color: black; border: 2px solid #FFD966;")

    # Set the notch type when the buttons are clicked
    def set_notch_button_outline(button, notch):
        # Reset outline of all buttons
        for btn in [notch50, notch60, notchAll, notchNone]:
            btn.setStyleSheet("background-color: #E0E0E0; color: black;")

        # Set outline of clicked button to yellow
        button.setStyleSheet("background-color: #E0E0E0; color: black; border: 2px solid #FFD966;")
        settings_signals.notchChanged.emit(notch)    
    notch50.clicked.connect(lambda: set_notch_button_outline(notch50, "50"))
    notch60.clicked.connect(lambda: set_notch_button_outline(notch60, "60"))
    notchAll.clicked.connect(lambda: set_notch_button_outline(notchAll, "50 + 60"))
    notchNone.clicked.connect(lambda: set_notch_button_outline(notchNone, "None"))

    notch_layout.addWidget(notch50)
    notch_layout.addWidget(notch60)
    notch_layout.addWidget(notchAll)
    notch_layout.addWidget(notchNone)
    notch_layout.addStretch(1)
    software_layout.addLayout(notch_layout)

    # Channels layout #
    channels_layout = QHBoxLayout()
    channels_label = QLabel("Channels: ")
    channels_layout.addWidget(channels_label, alignment=QtCore.Qt.AlignTop)

    # Create a table for the channels
    table = QtWidgets.QTableWidget(9, 4)
    table.setHorizontalHeaderLabels(["Start (Hz)", "Stop (Hz)", "Type", "Order"])
    header_font = table.horizontalHeader().font()
    header_font.setPointSize(12)
    table.horizontalHeader().setFont(header_font)
    table.setVerticalHeaderLabels(["All", "1", "2", "3", "4", "5", "6", "7", "8"])
    table.verticalHeader().setFont(header_font)
    table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    table.setFixedSize(800, 500)

    # Create a start input cell within the table
    def create_start_input(row, start_value, index):
        start_input = QtWidgets.QLineEdit(str(start_value))
        start_input.setAlignment(QtCore.Qt.AlignCenter)
        table.setCellWidget(row, index, start_input)
        return start_input
        
    start0_input = create_start_input(0, start0, 0)
    start1_input = create_start_input(1, start1, 0)
    start2_input = create_start_input(2, start2, 0)
    start3_input = create_start_input(3, start3, 0)
    start4_input = create_start_input(4, start4, 0)
    start5_input = create_start_input(5, start5, 0)
    start6_input = create_start_input(6, start6, 0)
    start7_input = create_start_input(7, start7, 0)
    start8_input = create_start_input(8, start8, 0)

    stop0_input = create_start_input(0, stop0, 1)
    stop1_input = create_start_input(1, stop1, 1)
    stop2_input = create_start_input(2, stop2, 1)
    stop3_input = create_start_input(3, stop3, 1)
    stop4_input = create_start_input(4, stop4, 1)
    stop5_input = create_start_input(5, stop5, 1)
    stop6_input = create_start_input(6, stop6, 1)
    stop7_input = create_start_input(7, stop7, 1)
    stop8_input = create_start_input(8, stop8, 1)

    order0_input = create_start_input(0, order0, 3)
    order1_input = create_start_input(1, order1, 3)
    order2_input = create_start_input(2, order2, 3)
    order3_input = create_start_input(3, order3, 3)
    order4_input = create_start_input(4, order4, 3)
    order5_input = create_start_input(5, order5, 3)
    order6_input = create_start_input(6, order6, 3)
    order7_input = create_start_input(7, order7, 3)
    order8_input = create_start_input(8, order8, 3)

    # Function to change the start value when changed
    def update_start(start):
        global start0, start1, start2, start3, start4, start5, start6, start7, start8
        if start == "start0":
            start0 = int(start0_input.text() or "0")
            start1_input.setText(str(start0))
            start2_input.setText(str(start0))
            start3_input.setText(str(start0))
            start4_input.setText(str(start0))
            start5_input.setText(str(start0))
            start6_input.setText(str(start0))
            start7_input.setText(str(start0))
            start8_input.setText(str(start0))
        elif start == "start1":
            start1 = int(start1_input.text() or "0")
        elif start == "start2":
            start2 = int(start2_input.text() or "0")
        elif start == "start3":
            start3 = int(start3_input.text() or "0")
        elif start == "start4":
            start4 = int(start4_input.text() or "0")
        elif start == "start5":
            start5 = int(start5_input.text() or "0")
        elif start == "start6":
            start6 = int(start6_input.text() or "0")
        elif start == "start7":
            start7 = int(start7_input.text() or "0")
        elif start == "start8":
            start8 = int(start8_input.text() or "0")

    # Connect the start input to the function
    start0_input.textChanged.connect(lambda: update_start("start0"))
    start1_input.textChanged.connect(lambda: update_start("start1"))
    start2_input.textChanged.connect(lambda: update_start("start2"))
    start3_input.textChanged.connect(lambda: update_start("start3"))
    start4_input.textChanged.connect(lambda: update_start("start4"))
    start5_input.textChanged.connect(lambda: update_start("start5"))
    start6_input.textChanged.connect(lambda: update_start("start6"))
    start7_input.textChanged.connect(lambda: update_start("start7"))
    start8_input.textChanged.connect(lambda: update_start("start8"))

    # Function to change the stop value when changed
    def update_stop(stop):
        global stop0, stop1, stop2, stop3, stop4, stop5, stop6, stop7, stop8
        if stop == "stop0":
            stop0 = int(stop0_input.text() or "0")
            stop1_input.setText(str(stop0))
            stop2_input.setText(str(stop0))
            stop3_input.setText(str(stop0))
            stop4_input.setText(str(stop0))
            stop5_input.setText(str(stop0))
            stop6_input.setText(str(stop0))
            stop7_input.setText(str(stop0))
            stop8_input.setText(str(stop0))
        elif stop == "stop1":
            stop1 = int(stop1_input.text() or "0")
        elif stop == "stop2":
            stop2 = int(stop2_input.text() or "0")
        elif stop == "stop3":
            stop3 = int(stop3_input.text() or "0")
        elif stop == "stop4":
            stop4 = int(stop4_input.text() or "0")
        elif stop == "stop5":
            stop5 = int(stop5_input.text() or "0")
        elif stop == "stop6":
            stop6 = int(stop6_input.text() or "0")
        elif stop == "stop7":
            stop7 = int(stop7_input.text() or "0")
        elif stop == "stop8":
            stop8 = int(stop8_input.text() or "0")
        
    # Connect the stop input to the function
    stop0_input.textChanged.connect(lambda: update_stop("stop0"))
    stop1_input.textChanged.connect(lambda: update_stop("stop1"))
    stop2_input.textChanged.connect(lambda: update_stop("stop2"))
    stop3_input.textChanged.connect(lambda: update_stop("stop3"))
    stop4_input.textChanged.connect(lambda: update_stop("stop4"))
    stop5_input.textChanged.connect(lambda: update_stop("stop5"))
    stop6_input.textChanged.connect(lambda: update_stop("stop6"))
    stop7_input.textChanged.connect(lambda: update_stop("stop7"))
    stop8_input.textChanged.connect(lambda: update_stop("stop8"))

    # Function to change the order value when changed
    def update_order(order):
        global order0, order1, order2, order3, order4, order5, order6, order7, order8
        if order == "order0":
            order0 = int(order0_input.text() or "0")
            order1_input.setText(str(order0))
            order2_input.setText(str(order0))
            order3_input.setText(str(order0))
            order4_input.setText(str(order0))
            order5_input.setText(str(order0))
            order6_input.setText(str(order0))
            order7_input.setText(str(order0))
            order8_input.setText(str(order0))
        elif order == "order1":
            order1 = int(order1_input.text() or "0")
        elif order == "order2":
            order2 = int(order2_input.text() or "0")
        elif order == "order3":
            order3 = int(order3_input.text() or "0")
        elif order == "order4":
            order4 = int(order4_input.text() or "0")
        elif order == "order5":
            order5 = int(order5_input.text() or "0")
        elif order == "order6":
            order6 = int(order6_input.text() or "0")
        elif order == "order7":
            order7 = int(order7_input.text() or "0")
        elif order == "order8":
            order8 = int(order8_input.text() or "0")

    # Connect the order input to the function
    order0_input.textChanged.connect(lambda: update_order("order0"))
    order1_input.textChanged.connect(lambda: update_order("order1"))
    order2_input.textChanged.connect(lambda: update_order("order2"))
    order3_input.textChanged.connect(lambda: update_order("order3"))
    order4_input.textChanged.connect(lambda: update_order("order4"))
    order5_input.textChanged.connect(lambda: update_order("order5"))
    order6_input.textChanged.connect(lambda: update_order("order6"))
    order7_input.textChanged.connect(lambda: update_order("order7"))
    order8_input.textChanged.connect(lambda: update_order("order8"))

    # Create a type dropdown cell within the table
    type_options = ["Butterworth", "Chebyshev", "Bessel"]
    def create_type_dropdown(row, type_value):
        type_dropdown = QtWidgets.QComboBox()
        for index, value in enumerate(type_options):
            type_dropdown.addItem(value)
            if value == type_value:
                type_dropdown.setCurrentIndex(index)
        table.setCellWidget(row, 2, type_dropdown)

        return type_dropdown

    # Create a type dropdown for each channel
    type0_dropdown = create_type_dropdown(0, type0)
    type1_dropdown = create_type_dropdown(1, type1)
    type2_dropdown = create_type_dropdown(2, type2)
    type3_dropdown = create_type_dropdown(3, type3)
    type4_dropdown = create_type_dropdown(4, type4)
    type5_dropdown = create_type_dropdown(5, type5)
    type6_dropdown = create_type_dropdown(6, type6)
    type7_dropdown = create_type_dropdown(7, type7)
    type8_dropdown = create_type_dropdown(8, type8)

    # Function to change the type value when changed
    def type_chosen(type):
        global type0, type1, type2, type3, type4, type5, type6, type7, type8
        if type == "type0":
            type0 = str(type0_dropdown.currentText())
            type1_dropdown.setCurrentIndex(type0_dropdown.currentIndex())
            type2_dropdown.setCurrentIndex(type0_dropdown.currentIndex())
            type3_dropdown.setCurrentIndex(type0_dropdown.currentIndex())
            type4_dropdown.setCurrentIndex(type0_dropdown.currentIndex())
            type5_dropdown.setCurrentIndex(type0_dropdown.currentIndex())
            type6_dropdown.setCurrentIndex(type0_dropdown.currentIndex())
            type7_dropdown.setCurrentIndex(type0_dropdown.currentIndex())
            type8_dropdown.setCurrentIndex(type0_dropdown.currentIndex())
        elif type == "type1":
            type1 = str(type1_dropdown.currentText())
        elif type == "type2":
            type2 = str(type2_dropdown.currentText())
        elif type == "type3":
            type3 = str(type3_dropdown.currentText())
        elif type == "type4":
            type4 = str(type4_dropdown.currentText())
        elif type == "type5":
            type5 = str(type5_dropdown.currentText())
        elif type == "type6":
            type6 = str(type6_dropdown.currentText())
        elif type == "type7":
            type7 = str(type7_dropdown.currentText())
        elif type == "type8":
            type8 = str(type8_dropdown.currentText())

    # Connect the type dropdown to the function
    type0_dropdown.currentIndexChanged.connect(lambda: type_chosen("type0"))
    type1_dropdown.currentIndexChanged.connect(lambda: type_chosen("type1"))
    type2_dropdown.currentIndexChanged.connect(lambda: type_chosen("type2"))
    type3_dropdown.currentIndexChanged.connect(lambda: type_chosen("type3"))
    type4_dropdown.currentIndexChanged.connect(lambda: type_chosen("type4"))
    type5_dropdown.currentIndexChanged.connect(lambda: type_chosen("type5"))
    type6_dropdown.currentIndexChanged.connect(lambda: type_chosen("type6"))
    type7_dropdown.currentIndexChanged.connect(lambda: type_chosen("type7"))
    type8_dropdown.currentIndexChanged.connect(lambda: type_chosen("type8"))

    channels_layout.addWidget(table)
    software_layout.addLayout(channels_layout)

    # 3 buttons layout #
    submit_layout = QHBoxLayout()
    submit_button = QPushButton("Save")
    load_button = QPushButton("Load")
    reset_button = QPushButton("Reset")
    submit_button.setCheckable(True)
    load_button.setCheckable(True)
    reset_button.setCheckable(True)
    submit_button.setFixedSize(150, 50)
    load_button.setFixedSize(150, 50)
    reset_button.setFixedSize(150, 50)
    submit_button.setStyleSheet("background-color: black; color: white;")
    load_button.setStyleSheet("background-color: black; color: white;")
    reset_button.setStyleSheet("background-color: black; color: white;")

    # Function to reset the settings
    def reset_button_clicked():
        global isBandPass, isBandStop, notch
        bandpass_clicked()
        bandpass.setChecked(True)
        bandstop.setChecked(False)
        set_notch_button_outline(notch50, "50")
        for btn in [notch60, notchAll, notchNone]:
            btn.setChecked(False)
        notch50.setChecked(True)
        reset_button.setChecked(False)

    # Function to save the settings
    def submit_button_clicked():
        submit_button.setChecked(False)

    # Function to load the settings
    def load_button_clicked():
        load_button.setChecked(False)

    # Connect the buttons to the functions
    submit_button.clicked.connect(submit_button_clicked)
    reset_button.clicked.connect(reset_button_clicked)
    load_button.clicked.connect(load_button_clicked)
    submit_layout.addWidget(submit_button)
    submit_layout.addWidget(load_button)
    submit_layout.addWidget(reset_button)
    submit_layout.addStretch(1)
    software_layout.addLayout(submit_layout)

    # IMPEDANCE LAYOUT #
    impedance_layout = QHBoxLayout()
    impedance_layout.setAlignment(QtCore.Qt.AlignTop)

    # Check all #
    all_layout = QHBoxLayout()
    all_layout.setAlignment(QtCore.Qt.AlignTop)
    all_label = QLabel("Channels ")
    all_layout.addWidget(all_label)
    all_button = QPushButton("Check All")
    all_button.setStyleSheet("background-color: #E0E0E0; color: black;")
    all_button.setFixedSize(100, 50)
    all_layout.addWidget(all_button)

    impedance_layout.addLayout(all_layout)

    # Individual layout #
    spacer = QWidget()
    spacer.setFixedWidth(40)
    impedance_layout.addWidget(spacer)

    individual_layout = QVBoxLayout()

    # Channel 1
    channel1_layout = QHBoxLayout()
    channel1_label = QLabel("1 ")
    channel1_layout.addWidget(channel1_label)
    channel1_button = QPushButton("Check")
    channel1_button.setStyleSheet("background-color: #E0E0E0; color: black;")
    channel1_button.setFixedSize(100, 50)
    channel1_layout.addWidget(channel1_button)
    channel1_status = create_nav_button("./images/unchecked.png", 50, 50)
    channel1_layout.addWidget(channel1_status)
    channel1_impedance = QLabel(channel1_value)
    channel1_layout.addWidget(channel1_impedance)
    channel1_layout.addStretch(1)
    individual_layout.addLayout(channel1_layout)
    # Function to change the status of the channel when clicked
    def channel1_button_clicked():
        channel1_status.setIcon(QtGui.QIcon("./images/success.png"))
        channel1_value = "10kOhm"
        channel1_impedance.setText(channel1_value)
    channel1_button.clicked.connect(channel1_button_clicked)

    # Channel 2
    channel2_layout = QHBoxLayout()
    channel2_label = QLabel("2 ")
    channel2_layout.addWidget(channel2_label)
    channel2_button = QPushButton("Check")
    channel2_button.setStyleSheet("background-color: #E0E0E0; color: black;")
    channel2_button.setFixedSize(100, 50)
    channel2_layout.addWidget(channel2_button)
    channel2_status = create_nav_button("./images/unchecked.png", 50, 50)
    channel2_layout.addWidget(channel2_status)
    channel2_impedance = QLabel(channel2_value)
    channel2_layout.addWidget(channel2_impedance)
    channel2_layout.addStretch(1)   
    individual_layout.addLayout(channel2_layout)
    def channel2_button_clicked():
        channel2_status.setIcon(QtGui.QIcon("./images/fail.png"))
        channel2_value = "200kOhm"
        channel2_impedance.setText(channel2_value)
    channel2_button.clicked.connect(channel2_button_clicked)

    # Channel 3
    channel3_layout = QHBoxLayout()
    channel3_label = QLabel("3 ")
    channel3_layout.addWidget(channel3_label)
    channel3_button = QPushButton("Check")
    channel3_button.setStyleSheet("background-color: #E0E0E0; color: black;")
    channel3_button.setFixedSize(100, 50)
    channel3_layout.addWidget(channel3_button)
    channel3_status = create_nav_button("./images/unchecked.png", 50, 50)
    channel3_layout.addWidget(channel3_status)
    channel3_impedance = QLabel(channel3_value)
    channel3_layout.addWidget(channel3_impedance)
    channel3_layout.addStretch(1)   
    individual_layout.addLayout(channel3_layout)
    def channel3_button_clicked():
        channel3_status.setIcon(QtGui.QIcon("./images/success.png"))
        channel3_value = "10kOhm"
        channel3_impedance.setText(channel3_value)
    channel3_button.clicked.connect(channel3_button_clicked)

    # Channel 4
    channel4_layout = QHBoxLayout()
    channel4_label = QLabel("4 ")
    channel4_layout.addWidget(channel4_label)
    channel4_button = QPushButton("Check")
    channel4_button.setStyleSheet("background-color: #E0E0E0; color: black;")
    channel4_button.setFixedSize(100, 50)
    channel4_layout.addWidget(channel4_button)
    channel4_status = create_nav_button("./images/unchecked.png", 50, 50)
    channel4_layout.addWidget(channel4_status)
    channel4_impedance = QLabel(channel4_value)
    channel4_layout.addWidget(channel4_impedance)
    channel4_layout.addStretch(1)   
    individual_layout.addLayout(channel4_layout)
    def channel4_button_clicked():
        channel4_status.setIcon(QtGui.QIcon("./images/success.png"))
        channel4_value = "10kOhm"
        channel4_impedance.setText(channel4_value)
    channel4_button.clicked.connect(channel4_button_clicked)

    # Channel 5
    channel5_layout = QHBoxLayout()
    channel5_label = QLabel("5 ")
    channel5_layout.addWidget(channel5_label)
    channel5_button = QPushButton("Check")
    channel5_button.setStyleSheet("background-color: #E0E0E0; color: black;")
    channel5_button.setFixedSize(100, 50)
    channel5_layout.addWidget(channel5_button)
    channel5_status = create_nav_button("./images/unchecked.png", 50, 50)
    channel5_layout.addWidget(channel5_status)
    channel5_impedance = QLabel(channel5_value)
    channel5_layout.addWidget(channel5_impedance)
    channel5_layout.addStretch(1)   
    individual_layout.addLayout(channel5_layout)
    def channel5_button_clicked():
        channel5_status.setIcon(QtGui.QIcon("./images/success.png"))
        channel5_value = "10kOhm"
        channel5_impedance.setText(channel5_value)
    channel5_button.clicked.connect(channel5_button_clicked)

    # Channel 6
    channel6_layout = QHBoxLayout()
    channel6_label = QLabel("6 ")
    channel6_layout.addWidget(channel6_label)
    channel6_button = QPushButton("Check")
    channel6_button.setStyleSheet("background-color: #E0E0E0; color: black;")
    channel6_button.setFixedSize(100, 50)
    channel6_layout.addWidget(channel6_button)
    channel6_status = create_nav_button("./images/unchecked.png", 50, 50)
    channel6_layout.addWidget(channel6_status)
    channel6_impedance = QLabel(channel6_value)
    channel6_layout.addWidget(channel6_impedance)
    channel6_layout.addStretch(1)   
    individual_layout.addLayout(channel6_layout)
    def channel6_button_clicked():
        channel6_status.setIcon(QtGui.QIcon("./images/success.png"))
        channel6_value = "10kOhm"
        channel6_impedance.setText(channel6_value)
    channel6_button.clicked.connect(channel6_button_clicked)

    # Channel 7
    channel7_layout = QHBoxLayout()
    channel7_label = QLabel("7 ")
    channel7_layout.addWidget(channel7_label)
    channel7_button = QPushButton("Check")
    channel7_button.setStyleSheet("background-color: #E0E0E0; color: black;")
    channel7_button.setFixedSize(100, 50)
    channel7_layout.addWidget(channel7_button)
    channel7_status = create_nav_button("./images/unchecked.png", 50, 50)
    channel7_layout.addWidget(channel7_status)
    channel7_impedance = QLabel(channel7_value)
    channel7_layout.addWidget(channel7_impedance)
    channel7_layout.addStretch(1)   
    individual_layout.addLayout(channel7_layout)
    def channel7_button_clicked():
        channel7_status.setIcon(QtGui.QIcon("./images/success.png"))
        channel7_value = "10kOhm"
        channel7_impedance.setText(channel7_value)
    channel7_button.clicked.connect(channel7_button_clicked)

    # Channel 8
    channel8_layout = QHBoxLayout()
    channel8_label = QLabel("8 ")
    channel8_layout.addWidget(channel8_label)
    channel8_button = QPushButton("Check")
    channel8_button.setStyleSheet("background-color: #E0E0E0; color: black;")
    channel8_button.setFixedSize(100, 50)
    channel8_layout.addWidget(channel8_button)
    channel8_status = create_nav_button("./images/unchecked.png", 50, 50)
    channel8_layout.addWidget(channel8_status)
    channel8_impedance = QLabel(channel8_value)
    channel8_layout.addWidget(channel8_impedance)
    channel8_layout.addStretch(1)   
    individual_layout.addLayout(channel8_layout)
    def channel8_button_clicked():
        channel8_status.setIcon(QtGui.QIcon("./images/success.png"))
        channel8_value = "10kOhm"
        channel8_impedance.setText(channel8_value)
    channel8_button.clicked.connect(channel8_button_clicked)

    impedance_layout.addLayout(individual_layout)

    impedance_layout.addStretch(1)

    # Function to check all channels
    def all_button_clicked():
        for btn in [channel1_button, channel2_button, channel3_button, channel4_button, channel5_button, channel6_button, channel7_button, channel8_button]:
            btn.click()
    all_button.clicked.connect(all_button_clicked)

    # HARDWARE LAYOUT #
    hardware_layout = QVBoxLayout()
    hardware_layout.setAlignment(QtCore.Qt.AlignTop)

    # Create a table for 'Hardware'
    table2 = QtWidgets.QTableWidget(8, 5)
    table2.setHorizontalHeaderLabels(["Include Bias", "SRB1", "SRB2", "Input Type", "PGA Gain"])
    header_font = table2.horizontalHeader().font()
    header_font.setPointSize(12)
    table2.horizontalHeader().setFont(header_font)
    table2.setVerticalHeaderLabels(["1", "2", "3", "4", "5", "6", "7", "8"])
    table2.verticalHeader().setFont(header_font)
    table2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    table2.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    table2.setFixedSize(800, 500)

    # Create a dropdown options for each cell
    yes_options = ["Yes", "No"]
    on_options = ["On", "Off"]
    input_options = ["Normal","Shorted","Bias_Meas","MVDD","Temp","Test","Bias_Drp", "Bias_Drn"]
    pga_options = ["1", "2", "4", "8", "16", "24"]

    # Create a dropdown cell within the table
    def create_dropdown(row, column, type_value, options):
        dropdown = QtWidgets.QComboBox()
        for index, value in enumerate(options):
            dropdown.addItem(value)
            if value == str(type_value):
                dropdown.setCurrentIndex(index)
        table2.setCellWidget(row, column, dropdown)

        return dropdown

    bias1_dropdown = create_dropdown(0, 0, bias1, yes_options)
    bias2_dropdown = create_dropdown(1, 0, bias2, yes_options)
    bias3_dropdown = create_dropdown(2, 0, bias3, yes_options)
    bias4_dropdown = create_dropdown(3, 0, bias4, yes_options)
    bias5_dropdown = create_dropdown(4, 0, bias5, yes_options)
    bias6_dropdown = create_dropdown(5, 0, bias6, yes_options)
    bias7_dropdown = create_dropdown(6, 0, bias7, yes_options)
    bias8_dropdown = create_dropdown(7, 0, bias8, yes_options)

    srb11_dropdown = create_dropdown(0, 1, srb11, on_options)
    srb12_dropdown = create_dropdown(1, 1, srb12, on_options)
    srb13_dropdown = create_dropdown(2, 1, srb13, on_options)
    srb14_dropdown = create_dropdown(3, 1, srb14, on_options)
    srb15_dropdown = create_dropdown(4, 1, srb15, on_options)
    srb16_dropdown = create_dropdown(5, 1, srb16, on_options)
    srb17_dropdown = create_dropdown(6, 1, srb17, on_options)
    srb18_dropdown = create_dropdown(7, 1, srb18, on_options)

    srb21_dropdown = create_dropdown(0, 2, srb21, on_options)
    srb22_dropdown = create_dropdown(1, 2, srb22, on_options)
    srb23_dropdown = create_dropdown(2, 2, srb23, on_options)
    srb24_dropdown = create_dropdown(3, 2, srb24, on_options)
    srb25_dropdown = create_dropdown(4, 2, srb25, on_options)
    srb26_dropdown = create_dropdown(5, 2, srb26, on_options)
    srb27_dropdown = create_dropdown(6, 2, srb27, on_options)
    srb28_dropdown = create_dropdown(7, 2, srb28, on_options)

    input1_dropdown = create_dropdown(0, 3, input1, input_options)
    input2_dropdown = create_dropdown(1, 3, input2, input_options)
    input3_dropdown = create_dropdown(2, 3, input3, input_options)
    input4_dropdown = create_dropdown(3, 3, input4, input_options)
    input5_dropdown = create_dropdown(4, 3, input5, input_options)
    input6_dropdown = create_dropdown(5, 3, input6, input_options)
    input7_dropdown = create_dropdown(6, 3, input7, input_options)
    input8_dropdown = create_dropdown(7, 3, input8, input_options)

    pga1_dropdown = create_dropdown(0, 4, pga1, pga_options)
    pga2_dropdown = create_dropdown(1, 4, pga2, pga_options)
    pga3_dropdown = create_dropdown(2, 4, pga3, pga_options)
    pga4_dropdown = create_dropdown(3, 4, pga4, pga_options)
    pga5_dropdown = create_dropdown(4, 4, pga5, pga_options)
    pga6_dropdown = create_dropdown(5, 4, pga6, pga_options)
    pga7_dropdown = create_dropdown(6, 4, pga7, pga_options)
    pga8_dropdown = create_dropdown(7, 4, pga8, pga_options)

    # Functions to update the dropdown values
    def update_bias(bias):
        global bias1, bias2, bias3, bias4, bias5, bias6, bias7, bias8
        if bias == "bias1":
            bias1 = str(bias1_dropdown.currentText())
        elif bias == "bias2":
            bias2 = str(bias2_dropdown.currentText())
        elif bias == "bias3":
            bias3 = str(bias3_dropdown.currentText())
        elif bias == "bias4":
            bias4 = str(bias4_dropdown.currentText())
        elif bias == "bias5":
            bias5 = str(bias5_dropdown.currentText())
        elif bias == "bias6":
            bias6 = str(bias6_dropdown.currentText())
        elif bias == "bias7":
            bias7 = str(bias7_dropdown.currentText())
        elif bias == "bias8":
            bias8 = str(bias8_dropdown.currentText()) 

    def update_srb1(srb):
        global srb11, srb12, srb13, srb14, srb15, srb16, srb17, srb18
        if srb == "srb11":
            srb11 = str(srb11_dropdown.currentText())
        elif srb == "srb12":
            srb12 = str(srb12_dropdown.currentText())
        elif srb == "srb13":
            srb13 = str(srb13_dropdown.currentText())
        elif srb == "srb14":
            srb14 = str(srb14_dropdown.currentText())
        elif srb == "srb15":
            srb15 = str(srb15_dropdown.currentText())
        elif srb == "srb16":
            srb16 = str(srb16_dropdown.currentText())
        elif srb == "srb17":
            srb17 = str(srb17_dropdown.currentText())
        elif srb == "srb18":
            srb18 = str(srb18_dropdown.currentText())
    
    def update_srb2(srb):
        global srb21, srb22, srb23, srb24, srb25, srb26, srb27, srb28
        if srb == "srb21":
            srb21 = str(srb21_dropdown.currentText())
        elif srb == "srb22":
            srb22 = str(srb22_dropdown.currentText())
        elif srb == "srb23":
            srb23 = str(srb23_dropdown.currentText())
        elif srb == "srb24":
            srb24 = str(srb24_dropdown.currentText())
        elif srb == "srb25":
            srb25 = str(srb25_dropdown.currentText())
        elif srb == "srb26":
            srb26 = str(srb26_dropdown.currentText())
        elif srb == "srb27":
            srb27 = str(srb27_dropdown.currentText())
        elif srb == "srb28":
            srb28 = str(srb28_dropdown.currentText())

    def update_input(input):
        global input1, input2, input3, input4, input5, input6, input7, input8
        if input == "input1":
            input1 = str(input1_dropdown.currentText())
        elif input == "input2":
            input2 = str(input2_dropdown.currentText())
        elif input == "input3":
            input3 = str(input3_dropdown.currentText())
        elif input == "input4":
            input4 = str(input4_dropdown.currentText())
        elif input == "input5":
            input5 = str(input5_dropdown.currentText())
        elif input == "input6":
            input6 = str(input6_dropdown.currentText())
        elif input == "input7":
            input7 = str(input7_dropdown.currentText())
        elif input == "input8":
            input8 = str(input8_dropdown.currentText())

    def update_pga(pga):
        global pga1, pga2, pga3, pga4, pga5, pga6, pga7, pga8
        if pga == "pga1":
            pga1 = int(pga1_dropdown.currentText())
        elif pga == "pga2":
            pga2 = int(pga2_dropdown.currentText())
        elif pga == "pga3":
            pga3 = int(pga3_dropdown.currentText())
        elif pga == "pga4":
            pga4 = int(pga4_dropdown.currentText())
        elif pga == "pga5":
            pga5 = int(pga5_dropdown.currentText())
        elif pga == "pga6":
            pga6 = int(pga6_dropdown.currentText())
        elif pga == "pga7":
            pga7 = int(pga7_dropdown.currentText())
        elif pga == "pga8":
            pga8 = int(pga8_dropdown.currentText())

    # Connect the dropdowns to the functions
    bias1_dropdown.currentIndexChanged.connect(lambda: update_bias("bias1"))
    bias2_dropdown.currentIndexChanged.connect(lambda: update_bias("bias2"))
    bias3_dropdown.currentIndexChanged.connect(lambda: update_bias("bias3"))
    bias4_dropdown.currentIndexChanged.connect(lambda: update_bias("bias4"))
    bias5_dropdown.currentIndexChanged.connect(lambda: update_bias("bias5"))
    bias6_dropdown.currentIndexChanged.connect(lambda: update_bias("bias6"))
    bias7_dropdown.currentIndexChanged.connect(lambda: update_bias("bias7"))
    bias8_dropdown.currentIndexChanged.connect(lambda: update_bias("bias8"))

    srb11_dropdown.currentIndexChanged.connect(lambda: update_srb1("srb11"))
    srb12_dropdown.currentIndexChanged.connect(lambda: update_srb1("srb12"))
    srb13_dropdown.currentIndexChanged.connect(lambda: update_srb1("srb13"))
    srb14_dropdown.currentIndexChanged.connect(lambda: update_srb1("srb14"))
    srb15_dropdown.currentIndexChanged.connect(lambda: update_srb1("srb15"))
    srb16_dropdown.currentIndexChanged.connect(lambda: update_srb1("srb16"))
    srb17_dropdown.currentIndexChanged.connect(lambda: update_srb1("srb17"))
    srb18_dropdown.currentIndexChanged.connect(lambda: update_srb1("srb18"))

    srb21_dropdown.currentIndexChanged.connect(lambda: update_srb2("srb21"))
    srb22_dropdown.currentIndexChanged.connect(lambda: update_srb2("srb22"))
    srb23_dropdown.currentIndexChanged.connect(lambda: update_srb2("srb23"))
    srb24_dropdown.currentIndexChanged.connect(lambda: update_srb2("srb24"))
    srb25_dropdown.currentIndexChanged.connect(lambda: update_srb2("srb25"))
    srb26_dropdown.currentIndexChanged.connect(lambda: update_srb2("srb26"))
    srb27_dropdown.currentIndexChanged.connect(lambda: update_srb2("srb27"))
    srb28_dropdown.currentIndexChanged.connect(lambda: update_srb2("srb28"))

    input1_dropdown.currentIndexChanged.connect(lambda: update_input("input1"))
    input2_dropdown.currentIndexChanged.connect(lambda: update_input("input2"))
    input3_dropdown.currentIndexChanged.connect(lambda: update_input("input3"))
    input4_dropdown.currentIndexChanged.connect(lambda: update_input("input4"))
    input5_dropdown.currentIndexChanged.connect(lambda: update_input("input5"))
    input6_dropdown.currentIndexChanged.connect(lambda: update_input("input6"))
    input7_dropdown.currentIndexChanged.connect(lambda: update_input("input7"))
    input8_dropdown.currentIndexChanged.connect(lambda: update_input("input8"))

    pga1_dropdown.currentIndexChanged.connect(lambda: update_pga("pga1"))
    pga2_dropdown.currentIndexChanged.connect(lambda: update_pga("pga2"))
    pga3_dropdown.currentIndexChanged.connect(lambda: update_pga("pga3"))
    pga4_dropdown.currentIndexChanged.connect(lambda: update_pga("pga4"))
    pga5_dropdown.currentIndexChanged.connect(lambda: update_pga("pga5"))
    pga6_dropdown.currentIndexChanged.connect(lambda: update_pga("pga6"))
    pga7_dropdown.currentIndexChanged.connect(lambda: update_pga("pga7"))
    pga8_dropdown.currentIndexChanged.connect(lambda: update_pga("pga8"))

    hardware_layout.addWidget(table2)

    # 3 buttons layout #
    submit2_layout = QHBoxLayout()
    save2_button = QPushButton("Save")
    load2_button = QPushButton("Load")
    send2_button = QPushButton("Send")
    save2_button.setCheckable(True)
    load2_button.setCheckable(True)
    send2_button.setCheckable(True)
    save2_button.setFixedSize(150, 50)
    load2_button.setFixedSize(150, 50)
    send2_button.setFixedSize(150, 50)
    save2_button.setStyleSheet("background-color: black; color: white;")
    load2_button.setStyleSheet("background-color: black; color: white;")
    send2_button.setStyleSheet("background-color: black; color: white;")

    # Function to save the settings
    def save2_button_clicked():
        save2_button.setChecked(False)

    # Function to load the settings
    def load2_button_clicked():
        load2_button.setChecked(False)

    # Function to send the settings
    def send2_button_clicked():
        send2_button.setChecked(False)

    # Connect the buttons to the functions
    save2_button.clicked.connect(save2_button_clicked)
    send2_button.clicked.connect(send2_button_clicked)
    load2_button.clicked.connect(load2_button_clicked)

    submit2_layout.addWidget(save2_button)
    submit2_layout.addWidget(load2_button)
    submit2_layout.addWidget(send2_button)
    submit2_layout.addStretch(1)
    hardware_layout.addLayout(submit2_layout)

    # Create a stacked layout for the 3 settings [CODE TO BE DUPLICATED WHEN CONNECTING THE DIFFERENT FRONTEND SCREENS TOGETHER]
    software_widget = QWidget()
    software_widget.setLayout(software_layout)
    impedance_widget = QWidget()
    impedance_widget.setLayout(impedance_layout)
    hardware_widget = QWidget()
    hardware_widget.setLayout(hardware_layout)
    stacked_layout = QtWidgets.QStackedLayout()
    stacked_layout.addWidget(software_widget)
    stacked_layout.addWidget(impedance_widget)
    stacked_layout.addWidget(hardware_widget)

    setting_layout.addLayout(buttons_layout)
    setting_layout.addLayout(stacked_layout)

    # Put together the pop up window
    pop_up_layout.addLayout(heading)
    spacer = QWidget()
    spacer.setFixedHeight(20)
    pop_up_layout.addWidget(spacer)
    setting_layout.addStretch(1)
    pop_up_layout.addLayout(setting_layout)

    # Center the pop up window
    center_window(pop_up)

    # Show the pop up window
    pop_up.show()

    return bandpass.isChecked(), bandstop.isChecked()