# -*- coding: utf-8 -*-
"""

@author: AdrienAntoinette
"""

import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  
import os  		  	   		   	 		  		  		    	 		 		   		 		    	   		   	 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		   	 		  		  		    	 		 		   		 		    	   		   	 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  



def compute_portvals(trades, sv=100000, commission=0,impact=0):
    #commission = 0
    #impact = 0
    
    prices = get_data(list(trades.columns), pd.date_range(pd.to_datetime(trades.index[0]), pd.to_datetime(trades.index[-1])))
    prices.drop(columns = 'SPY', inplace = True)
    stocks = list(prices.columns)
    prices['Cash'] = 1.0
    
    
    
    trades['cash'] = 0
    #prices['cash'] = 1
    for i in range(0,len(prices)-1):
        for j in stocks:
            trades['cash'].iloc[i] = -trades[j].iloc[i]*prices[j].iloc[i]- commission - impact*prices[j].iloc[i]*trades[j].iloc[i]
            #trades['cash'].iloc[i] = -trades[j].iloc[i]*prices[j].iloc[i]- commission + impact*prices[j].iloc[i]*trades[j].iloc[i]
    
    
    trades_cum = trades.copy()
    trades_cum['cash'].iloc[0] = trades_cum['cash'].iloc[0] + sv
    trades_cum = trades_cum.cumsum(axis=0)
    
    portval = trades_cum*prices.values
    portvals = portval.sum(axis=1)
    return portvals
 		  	   		   	 		  
def author():  		  	  
   

if __name__ == "__main__":       		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
     compute_portvals()
     author()
		  		    	 		 		   		 		  
