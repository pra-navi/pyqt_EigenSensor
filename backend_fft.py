import numpy as np
import time
import datetime
import os
import json
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QLabel, QTextEdit, QDockWidget, QLineEdit
from clean_eeg import CleanEeg
from eeg_interface import EegInterface
import digital_filter
from frontend_fft import initialize_plot, app, win

#####################
# Initialization
#####################
datastamp = -1
timestamp_offset = 0
datastamp_offset = 400
datastamp_sample = 0
eeg_counter = 0
refresh_interval_ms = 100
refresh_samples = int(refresh_interval_ms * 0.25)
full_view_s = 10
filter_params = [True, 5, 50, 4]
notch_on = True
cds_patch_offset = 0
cds_patch_offset_dly = 0

# Setup EEG Data collection parameters
serial_port = 9
get_eeg_period = 0.5
get_eeg_duration = get_eeg_period
refresh_counter = 0    # Count up refresh_counter. If refresh_counter == refresh_2_eeg_ratio, get more eeg data
refresh_2_eeg_ratio = np.floor(get_eeg_period*1000 / refresh_interval_ms)
wait_for_buffer = 0
wait_for_buffer_dly = 0
bool_noise_cancel = False
bool_sync_button = False
data = np.zeros((9,0))  # Setup empty data array
dirname = ''
bool_line0 = True
bool_line1 = True
bool_line2 = True
bool_line4 = True
bool_line5 = True
bool_line6 = True

# Create data structure for plotting, test cds.patch()
xs = np.arange(0, int(full_view_s*250))/250
y0 = np.zeros((int(full_view_s*250)))/250 # p0
y1 = np.zeros((int(full_view_s*250)))/250 # p1
y2 = np.zeros((int(full_view_s*250)))/250 # p2
y3 = np.zeros((int(full_view_s*250)))/250 # p3
y4 = np.zeros((int(full_view_s*250)))/250 # p4
y5 = np.zeros((int(full_view_s*250)))/250 # p5
y6 = np.zeros((int(full_view_s*250)))/250 # p6
y7 = np.zeros((int(full_view_s*250)))/250 # p7

data = np.zeros((9, 0))

# Initialization Functions
def setup_directories(record_datetime):
    global dirname
    dirname = 'data_' + record_datetime.replace('-', '').replace(':', '').replace(' ', '_').replace('.', '_')
    os.makedirs(dirname)
    print('Created new directory "{}"'.format(dirname))

def write_json(data):
    global dirname
    json_string = json.dumps(data, indent=4)
    with open(os.path.join(dirname, 'json_data.json'), 'w') as outfile:
        outfile.write(json_string)

def initialize_eeg(serial_port):
    print('Setup to run the EEG data collection from serial port COM{}'.format(serial_port))
    eeg = EegInterface(serial_port=serial_port)
    board_id = eeg.board.board_id
    sampling_freq = eeg.board.get_sampling_rate(board_id)
    device_name = eeg.board.get_device_name(board_id)
    version = eeg.board.get_version()
    record_datetime = str(datetime.datetime.now())

    eeg.prepare_board()
    eeg.start_stream()
    
    print('Ready board for EEG collection')
    print('Board ID = {}, Device = {}, Version = {}, Sampling Rate = {}'.format(board_id, device_name, version, sampling_freq))
    to_json = {'record_datetime': record_datetime,
               'board_id': board_id, 
               'device_name': device_name,
               'version': version,
               'com_port': serial_port,
               'get_eeg_period': get_eeg_period,
               'get_eeg_duration': get_eeg_duration}
    return eeg, to_json

def set_data():
    global data, xs, y0, y1, y2, y3, y4, y5, y6, y7
    data = np.zeros((9, len(xs)))
    data[0] = xs
    data[1] = y0
    data[2] = y1
    data[3] = y2
    data[4] = y3
    data[5] = y4
    data[6] = y5
    data[7] = y6
    data[8] = y7

# Constantly refresh code
def stream():
    global data, timestamp_offset, eeg_counter, datastamp, datastamp_sample, refresh_counter, refresh_2_eeg_ratio
    global wait_for_buffer, wait_for_buffer_dly, cds_patch_offset, cds_patch_offset_dly, dirname, xs, curves, plots
    global xs, y0, y1, y2, y3, y4, y5, y6, y7
    global data_loaded, eeg, filter_params, notch_on, data_loaded_fft
    global dirname

    # Constantly refresh values that have been changed on the frontend screen settings
    import frontend_fft
    import subprocess
    screen = frontend_fft.screen

    # Switch between screens
    if screen == 1:
        app.closeAllWindows()
        eeg.stop_stream()
        # there is a lag of approximately 20 seconds before the new window opens (this is the lag that happens everytime any backend file is run, even the initial file sent by you)
        subprocess.call(["python", "backend_timeseries.py"])
    elif screen == 3:
        app.closeAllWindows()
        eeg.stop_stream()
        subprocess.call(["python", "backend_classification.py"])

    # Load values from frontend_fft
    min_freq, max_freq = frontend_fft.min_freq, frontend_fft.max_freq 
    min_amp, max_amp = frontend_fft.min_amp, frontend_fft.max_amp 
    smooth = frontend_fft.smooth
    isFiltered = frontend_fft.isFiltered 

    # Update axis for the graphs based on frontend screen settings
    for i in range(1):
        plots[i].setXRange(min_freq, max_freq)
        plots[i].setYRange(min_amp, max_amp)

    # The below code is taken from the original backend file sent with bokeh, with slight changes
    datastamp += 1
    refresh_counter_temp = refresh_counter
    cds_patch_offset_dly = cds_patch_offset

    if data.shape[1] == 0:
        time.sleep(datastamp_offset / 250)
        print('Sleep for {}s'.format(datastamp_offset/250))
        data_loaded = eeg.get_recording_no_time(include_timestamp=True)
        # FFT
        N = data_loaded.shape[1]
        freq = np.fft.fftfreq(N, d=1/250)   # x-axis of FFT Plot
        data_loaded_fft = np.abs(np.fft.fft(data_loaded, axis=1))    # y-axis of FFT Plot

        data = np.copy(data_loaded_fft)
        print('Collected data with shape {}'.format(data.shape))
        datastamp_sample = datastamp_offset

    elif refresh_counter < refresh_2_eeg_ratio:
        refresh_counter_temp += 1
        print('EEG Data Collection: Counting: refresh_counter = {}'.format(refresh_counter))
        
    else:
        refresh_counter_temp = 1
        wait_for_buffer = 1
        if not os.path.exists(os.path.join(dirname, 'stop.txt')):
            eeg_counter += 1
            data_loaded = eeg.get_recording_no_time(include_timestamp=True)
            N = data_loaded.shape[1]
            freq = np.fft.fftfreq(N, d=1/250)   # x-axis of FFT Plot
            data_loaded_fft = np.abs(np.fft.fft(data_loaded, axis=1))    # y-axis of FFT Plot
            np.save(os.path.join(dirname, str(eeg_counter) + '.npy'), data_loaded_fft)
            print('EEG Data Collection: Saved {}'.format(str(eeg_counter) + '.npy'))
            print('EEG Data Collection: Shape of data_loaded = {}'.format(data_loaded_fft.shape))
        else:
            eeg.stop_stream()
            print('Killed EEG Data Collection on serial_port {} due to stop command'.format(serial_port))
    
    if wait_for_buffer == 0:
        print('Data refresh: Waiting to start, datastamp = {}'.format(datastamp))
    
    elif refresh_counter == 1:
        print('Data refresh: Not enough data, reading file {}.npy'.format(eeg_counter))
        print('Data refresh: Before Trim shape = {}'.format(data.shape))
        data = data[:, -datastamp_offset:]
        datastamp_sample = datastamp_offset # old data retained and added to new data
        print('Data refresh: After Trim shape = {}'.format(data.shape))
        print('Data refresh: datastamp = {}, timestamp_offset = {}'.format(datastamp, timestamp_offset))
        data = np.concatenate((data, data_loaded_fft), axis=1)
        print('Data refresh: After Concatenate shape = {}'.format(data.shape))
        
    if filter_params[0] is True:
        filtered_data = np.copy(np.expand_dims(data, axis=0))
        filtered_data = np.expand_dims(filtered_data, axis=0)
        filtered_data = np.transpose(filtered_data, (0, 1, 3, 2))
        filtered_data[:, :, :, 1:9] = digital_filter.perform_filter(filtered_data[:, :, :, 1:9], band_pass=filter_params, notch_filter=notch_on)
        filtered_data = np.transpose(filtered_data[0, 0], (1, 0))
    else:
        filtered_data = np.copy(data)

        
    # iCanClean Algorithm
    if bool_noise_cancel is True:
        clean_object = CleanEeg('iCanClean')
        filtered_data = clean_object.iCanClean(np.expand_dims(np.expand_dims(np.copy(filtered_data), axis=0), axis=0), noise_channel=3, threshold=0.1)[0,0]

    print('Plot Update: refresh_counter = {}, refresh_2_eeg_ratio = {}'.format(refresh_counter, refresh_2_eeg_ratio))   
    
    if wait_for_buffer_dly == 0:
        print('Plot Update: Still waiting before plotting')
        
    elif refresh_counter == refresh_2_eeg_ratio:
        len_to_end = len(filtered_data[0, datastamp_sample:])
        print('Plot Update: refresh_counter == refresh_2_eeg_ratio. len_to_end = {}'.format(len_to_end))
        y0 = filtered_data[0, datastamp_sample:datastamp_sample+len_to_end]  # Channel 1
        y1 = filtered_data[1, datastamp_sample:datastamp_sample+len_to_end]  # Channel 2
        y2 = filtered_data[2, datastamp_sample:datastamp_sample+len_to_end]  # Channel 3
        y3 = filtered_data[3, datastamp_sample:datastamp_sample+len_to_end]  # Channel 4
        y4 = filtered_data[4, datastamp_sample:datastamp_sample+len_to_end]  # Channel 5
        y5 = filtered_data[5, datastamp_sample:datastamp_sample+len_to_end]  # Channel 6
        y6 = filtered_data[6, datastamp_sample:datastamp_sample+len_to_end]  # Channel 7
        y7 = filtered_data[7, datastamp_sample:datastamp_sample+len_to_end]  # Channel 8
        xs = np.arange(timestamp_offset, timestamp_offset+len(y0))/250
        
        datastamp_sample = datastamp_sample + len_to_end
        timestamp_offset = (timestamp_offset + len(y0)) % int(full_view_s*250) # Test cds.patch()
        cds_patch_offset = (cds_patch_offset + len_to_end) % int(full_view_s*250)  # Test cds.patch()
        
    else:
        print('Plot Update: refresh_counter /= refresh_2_eeg_ratio')
        print('filtered_data[0, datastamp_sample:datastamp_sample+refresh_samples] length = {}'.format(len(filtered_data[0, datastamp_sample:datastamp_sample+refresh_samples])))
        y0 = filtered_data[0, datastamp_sample:datastamp_sample+refresh_samples]  # Channel 1
        y1 = filtered_data[1, datastamp_sample:datastamp_sample+refresh_samples]  # Channel 2
        y2 = filtered_data[2, datastamp_sample:datastamp_sample+refresh_samples]  # Channel 3
        y3 = filtered_data[3, datastamp_sample:datastamp_sample+refresh_samples]  # Channel 4
        y4 = filtered_data[4, datastamp_sample:datastamp_sample+refresh_samples]  # Channel 5
        y5 = filtered_data[5, datastamp_sample:datastamp_sample+refresh_samples]  # Channel 6
        y6 = filtered_data[6, datastamp_sample:datastamp_sample+refresh_samples]  # Channel 7
        y7 = filtered_data[7, datastamp_sample:datastamp_sample+refresh_samples]  # Channel 8
        xs = np.arange(timestamp_offset, timestamp_offset+len(y0))/250
        
        datastamp_sample = datastamp_sample+refresh_samples
        timestamp_offset = (timestamp_offset + len(y0)) % int(full_view_s*250) # Test cds.patch()
        cds_patch_offset = (cds_patch_offset +  refresh_samples)% int(full_view_s*250) # Test cds.patch()
        
    print('Datastamp value = {}'.format(datastamp))
    print('Timestamp_offset time = {} s'.format(timestamp_offset/250))
    print('######################################\n')
    ##############################

    refresh_counter = refresh_counter_temp
    wait_for_buffer_dly = wait_for_buffer

    # Update the curves based on the new dataset
    xs = xs*25000
    xs = xs.astype(int)
    xs = (xs % int(full_view_s*25000))/25000
    curves[0].setData(xs, y0)
    curves[1].setData(xs, y1)
    curves[2].setData(xs, y2)
    curves[3].setData(xs, y3)
    curves[4].setData(xs, y4)
    curves[5].setData(xs, y5)
    curves[6].setData(xs, y6)
    curves[7].setData(xs, y7)

# Initialize EEG and plot
record_datetime = str(datetime.datetime.now())
setup_directories(record_datetime)

eeg, eeg_info = initialize_eeg(serial_port)

write_json(eeg_info)
set_data()

plots, curves = initialize_plot(data=data)

timer = QtCore.QTimer()
timer.timeout.connect(stream)
timer.start(refresh_interval_ms)

win.show()

app.exec_()

