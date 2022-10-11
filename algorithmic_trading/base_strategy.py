# -*- coding: utf-8 -*-
"""

@author: AdrienAntoinette
"""

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt	 
import random  
import marketsimcode as ms 
import rt as RT 
import bagging as bl
import indicators as ind

def trades_dataframe(prices, y_test):
    
    stocks = list(prices.columns)
    #Create the trades dataframe df
    trades= pd.DataFrame(np.zeros(len(prices)), index = prices.index, columns = stocks)
        
    for i in range(0,len(prices)-1):
        for j in stocks:
        
        #####price today is lower than tomorrow, buy
        ###Long 
            if y_test[i] == 1:
                if trades.cumsum(axis = 0).iloc[i][j] == 1000: 
                    trades.iloc[i][j] += 0 
                        
                elif trades.cumsum(axis = 0).iloc[i][j] == -1000: 
                    trades.iloc[i][j] += 2000 
                    
                elif trades.cumsum(axis = 0).iloc[i][j] == 0: 
                    trades.iloc[i][j] += 1000
            
            #price today is higher than tomorrow, sell
            ###short
            elif y_test[i] == -1:  
                if trades.cumsum(axis = 0).iloc[i][j] == 1000: 
                    trades.iloc[i][j] -= 2000 
                    
                elif trades.cumsum(axis = 0).iloc[i][j] == -1000: 
                    trades.iloc[i][j] -= 0 
                    
                elif trades.cumsum(axis = 0).iloc[i][j] == 0: 
                    trades.iloc[i][j] -= 1000 
                    
            ###cash 
            elif y_test[i] == 0:
                if trades.cumsum(axis = 0).iloc[i][j] == 1000: 
                    trades.iloc[i][j] -= 1000 
                    
                elif trades.cumsum(axis = 0).iloc[i][j] == -1000: 
                    trades.iloc[i][j] += 1000 
                    
                elif trades.cumsum(axis = 0).iloc[i][j] == 0: 
                    trades.iloc[i][j] -= 0
     
    return trades
 

def testPolicy(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31), sv=100000):
    # symbol="JPM"
    # sd=dt.datetime(2008, 1, 1)
    # ed=dt.datetime(2009,12,31)
    
    sma_lookback = 15 
    
    short_macd = 12
    long_macd = 26
    sig_lookback = 9
    
    lookback = 15
    
    #sd = sd - dt.timedelta(days=50)
    
    #15
    #12,9,26
    #10
    
    ###sma, macd, bbv
    sd2 = sd - dt.timedelta(days=50)
    
    
    sma = ind.SMA(symbol,sd2,ed, sma_lookback)
    
    macd = ind.MACD(symbol,sd2,ed,short_macd,long_macd, sig_lookback)
    
    bbv = ind.BBands(symbol,sd2,ed, lookback)
    
    
    signals = pd.DataFrame({'sma':sma, 'macd': macd, 'bbv': bbv}) #.reset_index(inplace=True)
    
    signals = signals[signals.index >= sd]
    #signals = signals[signals.index >= '2008-01-01']
    
    
    y_manual = np.zeros(len(signals))
    for i in range(0,len(signals)-1):
        
        # if macd.iloc[i] >= 0.01 or bbv.iloc[i] <= -0.80 or sma.iloc[i] <= 0.60:
        #     y_manual[i] = 1
        # elif macd.iloc[i] <= -0.01 or bbv.iloc[i] >= 0.80 or sma.iloc[i] >= 1:
        #     y_manual[i] = -1
        # else:
        #     y_manual[i] = 0
        a = 0 
        b = 0 
        c = 0 
        if macd.iloc[i] >= 0.15:      #0.15
            a = 1
        elif macd.iloc[i] <= -0.15:     #0.15
            a = -1
        else:
            a = 0
         
            
        if bbv.iloc[i] <= -0.9:      ##-0.8
            b = 1
        elif bbv.iloc[i] >= 0.9:     ###0.8
            b = -1
        else:
            b = 0
            
        if sma.iloc[i] <= 0.90:
            c = 1
        elif sma.iloc[i] > 1:
            c = -1 
        else:
            c = 0
            
        if a+b+c >= 2:
            y_manual[i] = 1
        elif a+b+c <=-2:
            y_manual[i] = -1 
        else:
            y_manual[i] = 0
                             
                                                                                                                                                                                                                                  
    
            
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]       
    prices = pd.DataFrame(prices)
    
    trades = trades_dataframe(prices, y_manual)
            
    return trades  #, prices , y_manual, signals 
    
# prices_manual = get_data([symbol],pd.date_range(sd , ed)) 

# prices_manual = prices_manual[symbol]
    
# prices_manual = pd.DataFrame(prices_manual)

# #prices_manual = prices_manual[prices_manual.index >= '2008-01-01']
# #prices_jpm_train = prices_df.iloc[0:len(prices_df)-N]

# #y_train = model.query(data_x)

# trades = trades_dataframe(prices_manual, y_manual)

            

def benchmark(symbol,sd,ed,sv):
       
   # symbol="JPM"
   # sd=dt.datetime(2008, 1, 1)
   # ed=dt.datetime(2009,12,31)
   # sv = 100000 	  	   		   	 		  		  		    	 		 		   		 		  
   	#Get price history for the stock  	   		   	 		  		  		    	 		 		   		 		       		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		         
       prices = get_data([symbol], pd.date_range(sd, ed))
       prices = prices[symbol]
       
       prices = pd.DataFrame(prices)
       
       stocks = list(prices.columns)
       
       benchmark_trades= pd.DataFrame(np.zeros(len(prices)), index = prices.index, columns = stocks)
       
       for i in stocks:
           benchmark_trades.iloc[0][i] += 1000
       
       return benchmark_trades
