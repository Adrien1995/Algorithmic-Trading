# -*- coding: utf-8 -*-
"""

@author: AdrienAntoinette
"""

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt


######SMA
def SMA(symbol,sd,ed, lookback):
    start_date = sd
    end_date = ed
    #symbol='JPM'
    #sd=dt.datetime(2008, 1, 1)
    #ed=dt.datetime(2009,12,31)
    
    prices = get_data([symbol],pd.date_range(start_date , end_date)) 
    
    prices = prices[symbol]    
    #lookback = 7
    
    #####SMA 
    
    sma = prices.rolling(window=lookback,min_periods=lookback).mean()
    
    sma_norm = sma/prices[0]   #sma[lookback]
    
    prices_norm = prices/prices[0]
    
    return prices/sma 
    


########Bolliner bands 
def BBands(symbol,sd,ed, lookback):
    start_date = sd
    end_date = ed
    prices = get_data([symbol],pd.date_range(start_date , end_date)) 
    
    prices = prices[symbol]
    
    sma = prices.rolling(window=lookback,min_periods=lookback).mean()
    
    sma_norm = sma/prices[0]   #sma[lookback]
    
    prices_norm = prices/prices[0]
    
    rolling_std = prices.rolling(window=lookback,min_periods=lookback).std()
    top_bd = sma + (2*rolling_std)
    top_bd_norm = top_bd/prices[0]
    bottom_bd = sma - (2*rolling_std)
    bottom_bd_norm = bottom_bd/prices[0]
    
    #bbp = (prices - bottom_bd)/(top_bd - bottom_bd)
    
    #bbv = (prices - sma)/(2*rolling_std)
    bbv = (prices-sma)/(2*rolling_std)
    
    return bbv 
    
    
#### MACD 
def MACD(symbol,sd,ed,short_lookback,long_lookback,sig_lookback):
    start_date = sd
    end_date = ed
    
    prices = get_data([symbol],pd.date_range(start_date , end_date)) 
    prices = prices[symbol] 
        
    long_ema = prices.ewm(span=long_lookback,min_periods=long_lookback,adjust=False).mean()
    short_ema = prices.ewm(span=short_lookback,min_periods=short_lookback,adjust=False).mean()
    sig_ema = prices.ewm(span=sig_lookback,min_periods=sig_lookback,adjust=False).mean()
    
    long_ema_norm = long_ema/prices[0]   #sma[lookback]
    short_ema_norm = short_ema/prices[0]
    
    sig_ema_norm = sig_ema/prices[0]
    
    prices_norm = prices/prices[0]
    
    return (short_ema-long_ema)/sig_ema
    


#########golden cross 
def golden_cross(symbol,sd,ed,short_lookback,long_lookback):
    start_date = sd
    end_date = ed
    #short_lookback = 15
    prices = get_data([symbol],pd.date_range(start_date , end_date)) 
    
    prices = prices[symbol]
    
    
    short_sma = prices.rolling(window=short_lookback,min_periods=short_lookback).mean()
    short_sma_norm = short_sma/prices[0]   #sma[lookback]
    
    #long_lookback = 50
    long_sma = prices.rolling(window=long_lookback,min_periods=long_lookback).mean()
    long_sma_norm = long_sma/prices[0]
    
    prices_norm = prices/prices[0]
   
    
    return (short_sma_norm - long_sma_norm)




####EMA 
def ema(symbol,sd,ed, lookback):
    start_date = sd
    end_date = ed
    
    prices = get_data([symbol],pd.date_range(start_date , end_date)) 
    
    prices = prices[symbol]
    
    ema = prices.ewm(span=lookback,min_periods=lookback,adjust=False).mean()
    
    ema_norm = ema/prices[0]   #sma[lookback]
    
    prices_norm = prices/prices[0]
    
    
    return ema_norm
    

# MACD(symbol,sd,ed,short_lookback, long_lookback)



if __name__ == "__main__":       		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
     SMA()
     BBands()
     golden_cross()
     ema()
     MACD()
     author()










