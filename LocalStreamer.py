# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 08:56:34 2018

@author: ayadav
"""

"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import time
from pylsl import StreamInfo, StreamOutlet


import numpy as np


from modules.read_csv import read



############################################
#                                          #
#           VARIABLES INIT                 #
#                                          #
############################################
# sampling frequency (how many samples per second)
fs = 250.0

# bandpass values
lowcut = 1.0
highcut = 50.0

# bandstop values
lowstop = 49.0
highstop = 51.0

# file with eeg data location
eeg_file = 'sampleData/OpenBCI-RAW-2018-08-21_13-47-49.csv'
#eeg_file = 'BlinkDemo.csv'
# seconds analysed
sec_beg = 100
sec_end = 200
sec_rng = sec_end-sec_beg

# lower and higher range values
rng = [sec_beg*int(fs), sec_end*int(fs)]

############################################
#                                          #
#          GET DATA FROM FILE              #
#                                          #
############################################
# read the eeg file to the list

# SNIFFER for detecting dialect
#with open(eeg_file, newline='') as csvfile:
#    dialect = csv.Sniffer().sniff(csvfile.read(1024))
#    csvfile.seek(0)
#    reader = csv.reader(csvfile, dialect)
    

data = read(
    eeg_file, delimiter=',', header=7, to_float=False, transpose=False,
    comas=False, mode='rt'
    )
#data = read(
#    eeg_file, delimiter=',', header=0, to_float=False, transpose=False,
#    comas=False, mode='rt'
#    )

# data extraction/ cleanup
data = zip(*data)
data = list(data)
# choose the channel
data = np.asanyarray(data[:12])
data = data.astype(np.float)

# first create a new stream info (here we set the name to BioSemi,
# the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
# last value would be the serial number of the device or some other more or
# less locally unique identifier for the stream as far as available (you
# could also omit it but interrupted connections wouldn't auto-recover)
info = StreamInfo('BioSemi', 'EEG', 8, 250, 'float32', 'myuid34234')

# next make an outlet
outlet = StreamOutlet(info)

print("now sending data...")
i=0
while True:
    
    mysample=[]
    # make a new random 8-channel sample; this is converted into a
    # pylsl.vectorf (the data type that is expected by push_sample)
    for j in range(1,data.__len__()-3):
        mysample.append(data[j][i])
    #mysample = [data[1][i], data[1][i], data[1][i], data[1][i], data[1][i], data[1][i], data[1][i], data[1][i]]
    # now send it and wait for a bit
#    mysample=[data[0][i]]
    outlet.push_sample(mysample)
    time.sleep(0.005)
    if i<data[0].__len__()-1:
        i=i+1
    else:
        i=0
