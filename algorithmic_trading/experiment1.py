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

import ManualStrategy as MS
import  StrategyLearner as SL 


def exp_1(symbol = "JPM",sd = dt.datetime(2008, 1, 1),ed = dt.datetime(2009,12,31)):

    ###benchmark - in sample 
    benchmark_trades = MS.benchmark(symbol , sd, ed, sv=100000)
    
    #benchmark_trades = benchmark_trades.iloc[0:len(benchmark_trades)-N]
    
    #benchmark_trades = benchmark_trades.iloc[long_lookback:]
    
    benchmark_val = ms.compute_portvals(benchmark_trades, sv=100000, commission=9.95, impact=0.05)
    
    benchmark_norm = pd.DataFrame(benchmark_val/benchmark_val[0])  
    
    
    ####straegy - in sample
    
    learner = SL.StrategyLearner()
    #learner.add_evidence()
    
    learner.add_evidence()	 		  
            
    strategy_val = learner.testPolicy(symbol,sd,ed,sv=100000)	
    
    trades_train = strategy_val.set_index(benchmark_trades.index)
    
    strategy_train = ms.compute_portvals(trades_train, sv=100000, commission=9.95,impact=0.05)
    
    strategy_norm = pd.DataFrame(strategy_train/strategy_train[0]) 
    
    
    ####manual - in sample 
    prices_manual = get_data([symbol],pd.date_range(sd , ed)) 
    
    prices_manual = prices_manual[symbol]
        
    prices_manual = pd.DataFrame(prices_manual)
    
    #prices_manual = prices_manual[prices_manual.index >= '2008-01-01']
    #prices_jpm_train = prices_df.iloc[0:len(prices_df)-N]
    
    #y_train = model.query(data_x)
    
    manual_val = MS.testPolicy(symbol, sd, ed , sv=100000)
    manual_train = ms.compute_portvals(manual_val, sv=100000, commission=9.95,impact=0.05)
    manual_norm = pd.DataFrame(manual_train/manual_train[0]) 
    #manual_train = MS.trades_dataframe(prices_manual, y_manual)
    
    plt.plot(benchmark_norm, color='g',label='Benchmark')
    #plt.plot(strategy_norm, color='r',label='Strategy')
    plt.plot(manual_norm, color='r',label='Manual')
    plt.plot(strategy_norm, color='y',label='Strategy')
    plt.legend(loc='upper left')
    plt.xlabel('Date') 
    plt.ylabel('Normalized Portfolio Value') 
    plt.title("Experiment 1: Comparison of & Manual Stragey vs Benchmark-in sample")
    #plt.legend(loc="upper left")
    #plt.grid(which='major', axis='both', linestyle='--')
    plt.xticks(rotation=45)
    #plt.show()
    
    plt.savefig("Fig5_Manua_Benchmark_insample.png", bbox_inches='tight')
    plt.close()   
    
        
    return benchmark_norm, strategy_norm, manual_norm, manual_val



