# -*- coding: utf-8 -*-
"""

@author: AdrienAntoinette
"""
import experiment1 as exp1
import experiment2 as exp2

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt	 
import random  
import marketsimcode as ms 
import rt as RT 
import bagging as bl
import indicators as ind

from pandas.plotting import table 


###Fig 1 
#in-sample manual and benchmark 
def manual_benchmark(symbol = "JPM",sd = dt.datetime(2008, 1, 1),ed = dt.datetime(2009,12,31)):

    ###benchmark - in sample 
    benchmark_trades = MS.benchmark(symbol , sd, ed, sv=100000)
    
    #benchmark_trades = benchmark_trades.iloc[0:len(benchmark_trades)-N]
    
    #benchmark_trades = benchmark_trades.iloc[long_lookback:]
    
    benchmark_val = ms.compute_portvals(benchmark_trades, sv=100000, commission=9.95, impact=0.05)
    
    benchmark_norm = pd.DataFrame(benchmark_val/benchmark_val[0])  
    
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
             
    return benchmark_norm, manual_norm, manual_val

benchmark_norm, manual_norm, manual_val = manual_benchmark(symbol = "JPM",sd = dt.datetime(2008, 1, 1),ed = dt.datetime(2009,12,31))
#plt.figure(1)
plt.plot(benchmark_norm, color='g',label='Benchmark')
#plt.plot(strategy_norm, color='r',label='Strategy')
plt.plot(manual_norm, color='r',label='Manual')

i = 0
j = 0
for idx, value in enumerate(manual_val.iloc[:,0].values):
        
        if value>0:
            i = i +1 
            if i == 1:
                plt.axvline(manual_val.index[idx], color="blue", linestyle="--", linewidth=0.75, label="Long")                
            else:
                plt.axvline(manual_val.index[idx], color="blue", linestyle="--", linewidth=0.75)
        elif value<0:
            j = j+1
            if j ==1:
                plt.axvline(manual_val.index[idx], color="black", linestyle="--", linewidth=0.75, label="Short")                
            else:
                plt.axvline(manual_val.index[idx], color="black", linestyle="--", linewidth=0.75)
plt.legend(loc='upper left')
plt.xlabel('Date') 
plt.ylabel('Normalized Portfolio Value') 
plt.title("Comparison of & Manual Stragey vs Benchmark-in sample")
plt.xticks(rotation=45)
#plt.show()
plt.savefig("Fig1_Manua_Benchmark_insample.png", bbox_inches='tight')
plt.close()

####Fig 2 
###out-of sample manual and benchmark 
benchmark_norm_out, manual_norm_out, manual_val_out = manual_benchmark(symbol = "JPM",sd = dt.datetime(2010, 1, 1),ed = dt.datetime(2011,12,31))
#plt.figure(2)
plt.plot(benchmark_norm_out, color='g',label='Benchmark')
#plt.plot(strategy_norm, color='r',label='Strategy')
plt.plot(manual_norm_out, color='r',label='Manual')
i = 0
j = 0
for idx, value in enumerate(manual_val_out.iloc[:,0].values):
        
        if value>0:
            i = i +1 
            if i == 1:
                plt.axvline(manual_val_out.index[idx], color="blue", linestyle="--", linewidth=0.75, label="Long")   
            else:
                plt.axvline(manual_val_out.index[idx], color="blue", linestyle="--", linewidth=0.75)
        elif value<0:
            j = j+1
            if j ==1:
                plt.axvline(manual_val_out.index[idx], color="black", linestyle="--", linewidth=0.75, label="Short")
                
            else:
                plt.axvline(manual_val_out.index[idx], color="black", linestyle="--", linewidth=0.75)
plt.legend(loc='upper left')
plt.xlabel('Date') 
plt.ylabel('Normalized Portfolio Value') 
plt.title("Comparison of & Manual Stragey vs Benchmark - out of sample")
plt.xticks(rotation=45)
plt.savefig("Fig2_Manua_Benchmark_outsample.png", bbox_inches='tight')
plt.close()

####Fig 3 
###in sample , out odf sample table for - benchmakr and manual strategy 
###CR,stdev, mean ofdaily return 

in_sample_benchmark_manual = [benchmark_norm, manual_norm]
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
    

stats = pd.DataFrame(columns = ['CR', 'Mean Daily Return', 'Sharpe Ratio'])
for i,j in enumerate(in_sample_benchmark_manual):
    #print(i,j)
    a,b,c = metrics(in_sample_benchmark_manual[i])
    
    stats = stats.append({'CR':a, 'Mean Daily Return' : b, 'Sharpe Ratio' : c },\
                         ignore_index=True)

stats2 = stats.T
stats2.columns = ['benchmark', 'manual']


ax = plt.subplot(311, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

table(ax, stats2)  # where df is your data frame
#plt.show()
plt.savefig('Fig3_insampletable.png', bbox_inches='tight')
plt.close()
    
#plt.table(stats)

####Fig 4 
out_sample_benchmark_manual = [benchmark_norm_out, manual_norm_out]
stats_out = pd.DataFrame(columns = ['CR', 'Mean Daily Return', 'Sharpe Ratio'])
for i,j in enumerate(out_sample_benchmark_manual):
    
    a,b,c = metrics(out_sample_benchmark_manual[i])
    
    stats_out = stats_out.append({'CR':a, 'Mean Daily Return' : b, 'Sharpe Ratio' : c },\
                         ignore_index=True)

stats2_out = stats_out.T
stats2_out.columns = ['benchmark', 'manual']

ax = plt.subplot(311, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

table(ax, stats2_out)  # where df is your data frame
#plt.show()
plt.savefig('Fig4_outsampleletable.png', bbox_inches='tight')
plt.close()


####Fig5

###Experiment 1 
####in sample strategy, manual, benchmark portoflo vlaues


exp1.exp_1(symbol = "JPM",sd = dt.datetime(2008, 1, 1),ed = dt.datetime(2009,12,31))

####Experiment - 2
###
#Fig 7
##table with how impact affect insam ple behavior 

exp2.exp2(symbol = "JPM",sd = dt.datetime(2008, 1, 1),ed = dt.datetime(2009,12,31))

##Fig 8 - optional, but add,
###Just the figs of those trades over time 

