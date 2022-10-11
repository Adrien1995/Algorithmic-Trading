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

import basestrategy as MS

from pandas.plotting import table 

def metrics(df):
    df = df / df.iloc[0]
    cr = df.iloc[-1]/df.iloc[0] -1
    adr = df[1:].pct_change().mean()
    sddr = df[1:].pct_change().std()
    sr = (adr/sddr)*(252**0.5)
    cr = "{:.4f}".format(cr[0])
    adr = "{:.4f}".format(adr[0])
    sddr = "{:.4f}".format(sddr[0])
    sr = "{:.4f}".format(sr[0])
    return cr,adr, sr 

def exp2(symbol = "JPM",sd = dt.datetime(2008, 1, 1),ed = dt.datetime(2009,12,31)):

    impact = [0,0.005, 0.010, 0.020]
    
    impact_dat = []
    
    for i in impact:
        learner = SL.StrategyLearner()
    #learner.add_evidence()
        
        learner.add_evidence()	 		  
                
        strategy_val = learner.testPolicy(symbol,sd,ed,sv=100000)	
        
        #trades_train = strategy_val.set_index(benchmark_trades.index)
        
        strategy_train = ms.compute_portvals(strategy_val, sv=100000, commission=0,impact=i)
        
        strategy_norm = pd.DataFrame(strategy_train/strategy_train[0]) 
        
        plt.plot(strategy_norm, label="impact {}".format(i))
        impact_dat.append(strategy_norm)
    

    plt.xticks(rotation=90)
    plt.legend(loc="upper left")
    #plt.grid(which='major', axis='both', linestyle='--')
    
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title("Experiment 2: StrategyLearner in-sample portfolio value with impact")
    
    plt.savefig("Fig6_Exp2_strategy_with_impact_insample.png", bbox_inches='tight')
    plt.close()  
        

# def metrics(df):
#     df = df / df.iloc[0]
#     cr = df.iloc[-1]/df.iloc[0] -1
#     adr = df[1:].pct_change().mean()
#     sddr = df[1:].pct_change().std()
#     sr = (adr/sddr)*(252**0.5)
#     return    cr, adr, sddr,sr #"{:.4f}".format(adr), "{:.4f}".format(sddr), "{:.4f}".format(sr)



    stats = pd.DataFrame(columns = ['Impact', 'CR', 'Mean Daily Return', 'Sharpe Ratio'])
    for i,j in enumerate(impact):
        #print(i,j)
        a,b,c = metrics(impact_dat[i])
        #print(a,b,c)
        #print('next)')
        stats = stats.append({'Impact' : j, 'CR':a, 'Mean Daily Return' : b, 'Sharpe Ratio' : c },\
                             ignore_index=True)
    
    
    
    stats2 = stats.T
    stats2.columns = ['measurement0', 'measurement1','measurement2', 'measurement3' ]
    
    ax = plt.subplot(311, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    
    table(ax, stats2)  # where df is your data frame
    #plt.show()
    plt.savefig("Fig7_Exp2_strategy_with_impact_insample_table.png", bbox_inches='tight')
    plt.close() 

