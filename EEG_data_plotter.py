# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 10:15:16 2018
#PLOTTER to Plot all Channels of EEG Data in realtime
@author: ayadav
"""
from scipy.cluster.vq import whiten
import serial

import matplotlib.pyplot as plt
import numpy as np
#For LSL Stream
from pylsl import StreamInlet, resolve_stream 

from sklearn import preprocessing
###################################################

#For BlinkDetector
import modules.filterlib as flt


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

# file with eeg data location for offline Analysis
eeg_file = 'OpenBCI-RAW-2018-08-06_11-20-41.csv'

# seconds analysed
sec_beg = 1
sec_end = 20
sec_rng = sec_end-sec_beg

# lower and higher range values
rng = [sec_beg*int(fs), sec_end*int(fs)]


def interpolate(x,x_min,x_max):
    if np.absolute(np.amax(x)) > x_max:
        interpolated_x=np.interp(x, (x.min(), x.max()), (x_min, x_max))
        return interpolated_x
    else:
        return x

def clamp(n, minn, maxn):
    if n < minn:
        return minn#0.01
    elif n > maxn:
        return maxn#0.01
    else:
        return n
    
fig, (ax,ax2) = plt.subplots(nrows=2, sharex=True)
def HeatMap(data):
    #plt.rcParams["figure.figsize"] = 5,2
    plt.cla()
    x = np.linspace(0,data.__len__(),data.__len__())
    y = data
    
#    fig, (ax,ax2) = plt.subplots(nrows=2, sharex=True)
    
    extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
    ax.imshow(y[np.newaxis,:], cmap="plasma", aspect="auto", extent=extent)
    ax.set_yticks([])
    ax.set_xlim(extent[0], extent[1])
    
    ax2.plot(x,y)

    plt.tight_layout()
    #plt.show()

def normalize(d):
    # d is a (n x dimension) np array
    d -= np.min(d, axis=0)
    d /= np.ptp(d, axis=0)
    return d

############################################
#                                          #
#           ONLINE FILTERING               #
#                                          #
############################################
def filtering(nChannel,data,paddedData, var_paddedData, lowstop, highstop, lowcut, highcut,fs=250):
        
         #get rid of Spikes and remove Mean from data
        data_rt=[]
        for i in data: #predictions:
            sample = clamp(i,-10000,10000)
            if sample>0:
                sample -= np.average(data)
            elif sample<0:    
                sample += np.average(data)
            else:
                sample=0.1
            data_rt.append(sample)
        data=data_rt           
       
        
       
        #Pad Data before Filtering 
        sampleSize=500
        paddedData.extend(data) #Select Channel
        if paddedData.__len__()>sampleSize:
            del paddedData[0:data.__len__()]
        
        padded_Data[nChannel]= paddedData[:]
        
        var_paddedData = np.var(paddedData)
        var_padded_Data[nChannel]= var_paddedData
        
        # filter data using butt bandstop 49-51 Hz filter (50Hz)
        flted_50_stop = flt.butter_bandstop_filter(
            paddedData, lowstop, highstop, fs, order=2
            )
        # filter prefiltered 50_stop data using 1-50 Hz bandpass filter
        flted_1_50_pass = flt.butter_bandpass_filter(
            flted_50_stop, lowcut, highcut, fs, order=2
            )
        #Standardise Data
        flted_1_50_pass /=np.std(flted_1_50_pass)

        #predictions=AR_Model(flted_1_50_pass[flted_1_50_pass.__len__()-50:])
        #Realtime Data without padding
        data_pass= flted_1_50_pass[flted_1_50_pass.__len__()-data.__len__():]
#        data_pass= flted_50_stop[flted_50_stop.__len__()-data.__len__():]
        #Standardise data_pass
        #data_pass /= np.std(data_pass)
        return data_pass, flted_1_50_pass

############################################
#                                          #
#        Connect to Aurdrino               #
#                                          #
############################################
try:
    ser = serial.Serial('COM5',9600)
except:
    print('Audrino Error')
############################################
#                                          #
#        GET DATA FROM LSL Stream          #
#                                          #
############################################

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])
channel_count = inlet.channel_count
#Channel Number
nChannel=0
#Sampling Frequency
fs = 250  #Hz
b_n=0

#Empty lists for Sliding Window 
padded_Data=[[]]*channel_count#For Filtering
curves=[] #for AR
var_padded_Data= [100000]*channel_count #Initilise variance to let all Signals through
n_data_pass=[[]]*channel_count
n_flted_1_50_pass=[[]]*channel_count
tm_result=[[]]*channel_count



from pylsl import StreamInlet, resolve_stream, local_clock
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

# Create the pyqtgraph window
plot_duration = 10
## Switch to using white background and black foreground
pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'w')

win = pg.GraphicsWindow()
win.setWindowTitle('EEG Data Plotter: ' + inlet.info().name())
plt = win.addPlot()
#plt.setLimits(xMin=0.0, xMax=plot_duration, yMin=-10.0 * (inlet.channel_count - 1), yMax=10.0)

t0 = [local_clock()] * inlet.channel_count
curves = []
color=['b', 'g', 'r', 'c', 'm', 'y', 'w', 'b']
for ch_ix in range(inlet.channel_count):
    curves += [plt.plot(pen=color[ch_ix])]

def update():
    global inlet, curves, t0, padded_Data, var_padded_Data
    sample,timestamp= inlet.pull_chunk(timeout=0.0,max_samples=32)
    if timestamp:
        eegData=np.asanyarray(sample)            #Convert EEG Data into numpy Array
        eegWhite=whiten(eegData)                #Whiten the EEG Data
        
        timestamps= np.asanyarray(timestamp)     #Convert timestamp into numpy Array
        nChannelData=eegWhite.T                   #Comple EEG Data as an array
       
        for nChannel in range(channel_count):
            data = nChannelData[nChannel]      #Get single Channel EEG Data
            pa_d=padded_Data[nChannel][:]
            nChan=nChannel
            data_pass,flted_1_50_pass = filtering( nChan,data,pa_d, var_padded_Data[nChannel],
                                                          lowstop,
                                                          highstop, lowcut,
                                                          highcut, fs=250)
            n_flted_1_50_pass[nChannel]=flted_1_50_pass
            
            
            data_pass = interpolate(data_pass,-1,1)
            #data_pass=np.clip(np.asanyarray(data_pass),-1,1)
            #print(np.amax(flted_1_50_pass))
            #data_pass=np.clip(np.asanyarray(data_pass),-10,10)
            n_data_pass[nChannel]=data_pass
        
        n_data_pass1= preprocessing.normalize(np.asanyarray(n_data_pass))
        
        y=n_data_pass1
        y=y.T
        #Data Plotter
        for ch_ix in range(inlet.channel_count):
            old_x, old_y = curves[ch_ix].getData()
            if old_x is not None:
                old_x += t0[ch_ix]  # Undo t0 subtraction
                this_x = np.hstack((old_x, timestamps))
                this_y = np.hstack((old_y, y[:, ch_ix] -5*ch_ix))
            else:
                this_x = timestamps
                this_y = y[:, ch_ix] -5*ch_ix
                
            t0[ch_ix] = this_x[-1] - plot_duration
            this_x -= t0[ch_ix]
            b_keep = this_x >= 0
            curves[ch_ix].setData(this_x[b_keep], this_y[b_keep])


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5)


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


#Matplotlib version works fine but too Slow
#############################################
##                                          #
##           Data Aquisition Loop           #
##                                          #
#############################################
#while True:
#    # get a new sample (you can also omit the timestamp part if you're not
#    # interested in it)
#    #sample,timestamp = inlet.pull_sample()
#   
#    sample,timestamp= inlet.pull_chunk(timeout=10.0,max_samples=50)
#    if timestamp:
#        eegData=np.asanyarray(sample)           #Convert EEG Data into numpy Array
#        time= np.asanyarray(timestamp)          #Convert timestamp into numpy Array
#        nChannelData=eegData.T                  #Comple EEG Data as an array
#        
#        for nChannel in range(4):
#            data = nChannelData[nChannel]      #Get single Channel EEG Data
#    #        padded_Data=np.pad(data, (2000,0), 'constant', constant_values=(0, 6))
#            data_pass,flted_1_50_pass = preprocessing(data,padded_Data[nChannel], var_padded_Data[nChannel],
#                                                          lowstop,
#                                                          highstop, lowcut,
#                                                          highcut, fs=250)
#            n_flted_1_50_pass[nChannel]=flted_1_50_pass
#            ############################################
#            #                                          #
#            #           Template Matching              #
#            #                                          #
#            ############################################
#            t_match = False
#            img_data = flted_1_50_pass[flted_1_50_pass.__len__()-150:]
#            try:
#                image = np.zeros((1,img_data.__len__()))
#                template = np.zeros((1, Blink[0][:70].__len__()))
#       
#                image[0] =np.asanyarray(img_data) 
#                template[0] =np.asanyarray(Blink[0][:70])
#                result = match_template(image, template, pad_input=True)
#                tm_result[nChannel]=result
#                print(np.amax(result))
#                if np.amax(result)>=0.98:
#                    t_match = True
#                    b_n = b_n+1
#                    b_n= b_n%4
#                    print(b_n)
#                    ser.write(str.encode(b_n.__str__()))
#                #HeatMap(result[0])
#    #            plt.subplot(311)
#    #            plt.cla()
#    #            plt.plot(result[0])
#    #            plt.title(b_n)
#    #            plt.pause(0.01)
#            except Exception:
#                print('M.E')
#                #raise
#    #        plt.subplot(312)
#    #        plt.cla()
#    #        plt.plot(data, '-g')
#                #sg.spectrogram(result[0], fs,ylim=20)
#    #        template = 0    
#    #        t_match, b_n = template_Matching(flted_1_50_pass,template)
#            
#            if t_match:
#                print(t_match,b_n)
#                #Mouse control
#                import pyautogui
#                screenWidth, screenHeight = pyautogui.size()
#                currentMouseX, currentMouseY = pyautogui.position()
#                pyautogui.doubleClick()
#        #####################################
#        
#        #####################################
#        for nChannel in range(channel_count):
#            plt.subplot(channel_count,1,nChannel+1)
#            plt.cla()
#            plt.plot(n_flted_1_50_pass[nChannel])
#            plt.pause(0.001)
#        
