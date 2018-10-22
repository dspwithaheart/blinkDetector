# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 10:15:16 2018

ONLINE BLINK DETECTION ON RAW EEG DATA 
USING RECURRENCE PLOT AND TEMPLATE MATCHING

DATA STREAMING USING LSL(Lab Streaming Layer)

py4j TO SEND SIGNALS(Blinks Detected) TO JAVA APPLICATION (in my case OPEN BCI GUI)

Java Class for using py4j 
########################################
import py4j.GatewayServer; 
boolean blink;
public class Stack {
    Stack(){}
    
    public void Blinker(boolean a){
      blink=a;
    }
    
}
    
public class StackEntryPoint {
    private Stack stack;
    public StackEntryPoint() {
      stack = new Stack();
    }
    public Stack getStack() {
        return stack;
    }
}
########################################
@author: ayadav
"""
#For Template Matching
import modules.RecurrencePlot as rp
import modules.TemplateMatching as tm

import matplotlib.pyplot as plt
import numpy as np

#For LSL Stream
from pylsl import StreamInlet, resolve_stream 


import modules.filterlib as flt #For Filtering EEG Data
import modules.DataCollection as dc #For loading Blink Templates

#For Connecting Python and Java applications
from time import sleep
from py4j.java_gateway import JavaGateway

############################################
#                                          #
#           Local Functions                #
#                                          #
############################################
def clamp(n, minn, maxn):
    if n < minn:
        return 0.01
    elif n > maxn:
        return 0.01
    else:
        return n

#Empty lists for Sliding Window 
padded_Data=[] #For Filtering
var_padded_Data= 100000 #Initilise variance to let all Signals through
def preprocessing(data,padded_Data, var_padded_Data, lowstop, highstop, lowcut, highcut,fs=250):
        
        #get rid of Spikes and remove Mean from data
        data_rt=[]
        for i in data: #predictions:
            sample = clamp(i,-var_padded_Data,var_padded_Data)
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
        padded_Data.extend(data) #Select Channel
        if padded_Data.__len__()>sampleSize:
            del padded_Data[0:data.__len__()]
        
        var_padded_Data = np.var(padded_Data)
        ############################################
        #                                          #
        #           ONLINE FILTERING               #
        #                                          #
        ############################################
        
        # filter data using butt bandstop 49-51 Hz filter (50Hz)
        flted_50_stop = flt.butter_bandstop_filter(
            padded_Data, lowstop, highstop, fs, order=2
            )
        # filter prefiltered 50_stop data using 1-50 Hz bandpass filter
        flted_1_50_pass = flt.butter_bandpass_filter(
            flted_50_stop, lowcut, highcut, fs, order=2
            )
       
        #Standardise Data
        flted_1_50_pass /=np.std(flted_1_50_pass)

        #Realtime Data without padding
        data_pass= flted_1_50_pass[flted_1_50_pass.__len__()-data.__len__():]
       
        return data_pass, flted_1_50_pass
    
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


############################################
#                                          #
#           VARIABLES INIT                 #
#                                          #
############################################

# bandpass values
lowcut = 1.0
highcut = 50.0

# bandstop values
lowstop = 49.0
highstop = 51.0

#Channel Number
nChannel=0

#Sampling Frequency
fs = 250  #Hz
b_n=0  #No of Blinks

#Empty lists for Sliding Window 
padded_Data=[] #For Filtering
var_padded_Data= 100000 #Initilise variance to let all Signals through
n_data_pass=[]
n_flted_1_50_pass=[]
############################################
#                                          #
#           Data Aquisition Loop           #
#                                          #
############################################

#Py4Java Connect to Java Gateway Server
#------------------------------------------#
gateway = JavaGateway()

try:
    stack = gateway.entry_point.getStack()
except Exception:
    print("JavaServer error")
#-----------------------------------------#

global nOfBlinks
nOfBlinks =0
index=0
bl_Detected = False
timer=0 #For detecting Single or Double Bilink

while True:
    # get a new sample 
    sample,timestamp= inlet.pull_chunk(timeout=10.0,max_samples=32)
    if timestamp:
        eegData=np.asanyarray(sample)           #Convert EEG Data into numpy Array
        time= np.asanyarray(timestamp)          #Convert timestamp into numpy Array
        nChannelData=eegData.T                  #Comple EEG Data as an array
        
       
        data = nChannelData[nChannel]       # Get single Channel EEG Data
        data= rp.moving_average(data)       # Apply MA Filter
        #Apply preprocessing(Bandpass and Notch Filters)
        data_pass,flted_1_50_pass = preprocessing(data,padded_Data, var_padded_Data,
                                                      lowstop,
                                                      highstop, lowcut,
                                                      highcut, fs=250)
        #Set Image Size 
        img_len = 150
        templates,b=dc.loadTemplates_from_csv('2018-09-06_09-45.csv') #Blinks Templates File in  Directory savedData 
        #Get averaged Blink Template
        t_mean=np.mean(templates, axis=0)
        
        if flted_1_50_pass.__len__()>img_len:
            #Get the latest 150  samples of raw filtered EEG Data
            img_data1 = flted_1_50_pass[flted_1_50_pass.__len__()-img_len:]
            #Calculate Recurrence plot after applying MA Filter for template and raw Sample
            tmp1=  rp.moving_average(t_mean)
            template= rp.rec_plot(tmp1, eps=0.2, steps=10)
            
            tmp= rp.moving_average(img_data1)
            img= rp.rec_plot(tmp, eps=0.2, steps=10)
            
            #Pad the Recurrence plot of filtered EEG Data for better Pattern Recognition
            def pad_with(vector, pad_width, iaxis, kwargs):
                pad_value = kwargs.get('padder', 0)
                vector[:pad_width[0]] = pad_value
                vector[-pad_width[1]:] = pad_value
                return vector
            img1 = np.pad(img, 5, pad_with)
            
           #Run Template Matching
            result ,t_match, b_n = tm.template_Matching(img,template)
#            plt.imshow(result)
#            plt.title(np.amax(result))
            
            #Center of the Recurrence Plot
            nmax=74     #ndimage.maximum_position(result)[0]
            
            #Set the window size and Position to look for Template Matchings return Value
            rs =result[nmax-10:nmax+10,nmax-10:nmax+10]
#            print('Overall:',np.amax(result), ' Inside:',np.amax(rs))
            
            #For detecting single or Double Blinks
            #Multiple Blinks will be rejected
            index=(index+1)%3
            timer= (timer+1)%10
            flag=True
            
            if (index==1 or index==2) and bl_Detected:
                flag = False
                bl_Detected = False
                timer=0
                
            if np.amax(rs) > 0.4 and flag : #Here 0.4 is the Threshold for detected Blinks
                nOfBlinks +=1
                bl_Detected = True
                print(np.amax(rs), 'Blink', nOfBlinks)
                #For Mouse control
                import pyautogui
                screenWidth, screenHeight = pyautogui.size()
                currentMouseX, currentMouseY = pyautogui.position()
                if nOfBlinks==1:
                    #BLINK = True
                    #Call the Methods of the Java Class
                    try:
                        stack.Blinker(True)
                        sleep(0.5)
                        stack.Blinker(False)
                    except Exception:
                        print("JavaServer error")
                        
                    pyautogui.click()
                    print(' Click')
                    
                elif nOfBlinks==2:
                    pyautogui.doubleClick()
                    print('Double Click')
            #set the timer length (here 10 loops) 
            if timer==9:
                nOfBlinks=0
            