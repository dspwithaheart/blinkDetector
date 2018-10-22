from scipy.signal import butter, lfilter
import numpy as np

'''
    Filtering library.
'''


############################################
#                                          #
#       Butterworth bandpass filter        #
#                                          #
############################################

# Numerator (b) and denominator (a) polynomials of the IIR filter
def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Linear filter application
def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

############################################
#                                          #
#       Butterworth bandstop filter        #
#                                          #
############################################

# Numerator (b) and denominator (a) polynomials of the IIR filter
def butter_bandstop(lowstop, highstop, fs, order=2):
    nyq = 0.5 * fs
    low = lowstop / nyq
    high = highstop / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    return b, a


# Linear filter application
def butter_bandstop_filter(data, lowstop, highstop, fs, order=2):
    b, a = butter_bandstop(lowstop, highstop, fs, order=order)
    y = lfilter(b, a, data)
    return y
