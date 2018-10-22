# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 09:04:00 2018

@author: ayadav
"""
#For AR MODEL
#####################################################
from pandas import Series
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
#####################################################

#####################################################
#                                                   #
#                      AR MODEL                     #
#                                                   #
#####################################################
curves=[]
def AR_Model(data):
    global curves
    #Sliding Window for Training Data 
    sampleSize=500
    curves.extend(data) #Select Channel
    if curves.__len__()>sampleSize:
        del curves[0:data.__len__()]
        
    #Convert Data into Padas Dataframe
    series = Series(curves)
    X = series.values
    
#    # split dataset
#    X = series.values
#    train, test = X[1:int(len(X)*.7)], X[int(len(X)*.7):]
    
#   # split dataset
    X = series.values
    train = X[:] 
    test = data
    
    # train autoregression
    model = AR(train)
    model_fit = model.fit()
    window = model_fit.k_ar
    coef = model_fit.params
    
    # walk forward over time steps in test
    history = train[len(train)-window:]
    history = [history[i] for i in range(len(history))]
    predictions = list()
    for t in range(len(test)):
    	length = len(history)
    	lag = [history[i] for i in range(length-window,length)]
    	yhat = coef[0]
    	for d in range(window):
    		yhat += coef[d+1] * lag[window-d-1]
    	obs = test[t]
    	predictions.append(yhat)
    	history.append(obs)
    	#print('predicted=%f, expected=%f' % (yhat, obs))
    error = mean_squared_error(test, predictions)
   # print('Test MSE: %.3f' % error)
    #Return
    return predictions
    # plot
#    plt.subplot(211)
#    plt.plot(test, color='yellow')
#    plt.plot(predictions, color='orange')
    #pyplot.show()
#End AR MODEl
################################################################## 
