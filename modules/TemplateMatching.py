# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 12:05:57 2018

@author: ayadav
"""
#For Template Matching
from skimage.feature import match_template
import numpy as np

t_match = False
numOfBlinks=0
def template_Matching(image,template):
    global numOfBlinks,t_match    
    try:
        result = match_template(image, template, pad_input=True)
        #print(np.amax(result))
        if np.amax(result)>=0.98:
            t_match = True
            numOfBlinks = numOfBlinks+1
        else:
            t_match = False
        return result, t_match, numOfBlinks
    except Exception:
        print('Mach Errror')


############################################
##    Decision Tree
############################################
#from sklearn import tree
#X1 =Blink_nStd[:7]
#X1.extend(cl[:66])
#Y1 = [1]*7
#Y1.extend([0]*66)
#clf = tree.DecisionTreeClassifier()
#clf = clf.fit(X1, Y1)
#rs=result[0][:150]
#ds=data000[1:151]
#ds=ds.astype(np.float)
#clf.predict([ds]*10) 
#   
#import graphviz 
#dot_data = tree.export_graphviz(clf, out_file=None) 
#graph = graphviz.Source(dot_data) 
#graph.render("iris") 
#
##Whitenoise
#mean = 0
#std = 1 
#num_samples = 10000
#samples = np.random.normal(mean, std, size=num_samples)
#
##Slice Array into equal sizes
#chunks = lambda l, n: [l[x: x+n] for x in range(0, len(l), n)]
#cl=chunks(samples, 150)