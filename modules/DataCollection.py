# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 10:15:16 2018

@author: ayadav
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

def loadTemplates_from_csv(filename): 
    filename='savedData/' + filename#2018-09-06_09-45.csv'
    with open(filename, 'rt') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        reader_a = []
        for row in reader:
             reader_a.append(np.asarray(row))
        reader_a= np.asarray(reader_a)
        reader_a = reader_a.astype(np.float)
        #reader_a = reader_a.tolist()
        reader_a /=np.std(reader_a)
        reader_b = []
        for row in reader_a:
            if np.amax(row)<2.5: # Exclude noisy Samples
                reader_b.append(row)
        reader_b= np.asarray(reader_b)
        reader_b = reader_b.astype(np.float)
#        plt.plot(reader_b.T)
#        plt.show()
        return reader_b, reader_a


##Slice Array into equal sizes
#chunks = lambda l, n: [l[x: x+n] for x in range(0, len(l), n)]
#cl=chunks(samples, 150)
##CSV WRITER
#image = np.asarray(cl[:273])
#with open(filename, 'at') as csvfile:
#    spamwriter = csv.writer(csvfile, delimiter=',',
#                            quotechar=' ', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
#    for item in image:
#        spamwriter.writerow(item)