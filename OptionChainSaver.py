import os,sys,argparse
import pandas as pd
import backtrader as bt
import multiprocessing
#os.chdir("D:\\Sandbox\StockCSV")
#%matplotlib widget
from nsepython import *
import json
from datetime import date
import time
from datetime import datetime
def get_atm_strike(symbol):
    payload = nse_optionchain_scrapper(symbol.upper())
    ltp = float(payload['records']['underlyingValue'])
    strike_price_list = [x['strikePrice'] for x in payload['records']['data']]
    atm_strike = sorted([[round(abs(ltp-i),2),i] for i in strike_price_list])[0][1]
    return atm_strike

def printAll(allstonks):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    dt_s=now.strftime("%Y%m%d")
    s_allstonks=set(allstonks)-set(['NIFTY', 'FINNIFTY', 'BANKNIFTY','NIFTYIT'])
   
    noSto=len(s_allstonks)
    i=0
    while(running_status()):
        try:
            t1=time.time()
    #printAll( stocklist)
   
            for stonk in s_allstonks:
                now = datetime.now()
                dt_string = now.strftime("%Y%m%d_%H%M%S")  
                symbol=stonk
                i=i+1
            #lot_size=nse_get_fno_lot_sizes(symbol)
                optionchain=(nse_optionchain_scrapper(symbol))
                optionchain_Json= (optionchain)
            #data_only=json.dumps(optionchain_Json['records']['data'])
                dict_only=optionchain_Json['records']['data']
            
                expiries=optionchain['records']['expiryDates']
                df=pd.json_normalize(dict_only)
                df=df[[ "PE.strikePrice", "PE.expiryDate", "PE.underlying", "PE.identifier", "PE.openInterest", "PE.changeinOpenInterest", "PE.pchangeinOpenInterest", "PE.totalTradedVolume", "PE.impliedVolatility", "PE.lastPrice", "PE.change", "PE.pChange", "PE.totalBuyQuantity", "PE.totalSellQuantity", "PE.bidQty", "PE.bidprice", "PE.askQty", "PE.askPrice", "PE.underlyingValue", "strikePrice", "expiryDate", "CE.strikePrice", "CE.expiryDate", "CE.underlying", "CE.identifier", "CE.openInterest", "CE.changeinOpenInterest", "CE.pchangeinOpenInterest", "CE.totalTradedVolume", "CE.impliedVolatility", "CE.lastPrice", "CE.change", "CE.pChange", "CE.totalBuyQuantity", "CE.totalSellQuantity", "CE.bidQty", "CE.bidprice", "CE.askQty", "CE.askPrice", "CE.underlyingValue"]]
                df=df.drop(["PE.underlying", "CE.underlying","PE.strikePrice", "PE.change", "PE.pChange", "CE.change", "CE.pChange","CE.strikePrice", "CE.expiryDate","PE.expiryDate", "PE.identifier", "CE.identifier","PE.changeinOpenInterest", "PE.pchangeinOpenInterest","CE.changeinOpenInterest", "CE.pchangeinOpenInterest", "PE.bidQty", "PE.bidprice", "PE.askQty", "PE.askPrice", "CE.bidQty", "CE.bidprice", "CE.askQty", "CE.askPrice"], axis=1)
                df['timestamp']=optionchain_Json['records']['timestamp']
                df['Stock']=stonk
            
                df.to_csv(dt_s+"_"+stonk+".csv", sep=',',mode='a',index=False,header=False)
                print("Done "+stonk+"  " +str(i)+" /"+str(noSto))  
            t2=time.time()-t1
            print(t2)        
            with open('logwriters.txt', 'a') as f:
                f.write("\n AT " +   str(now)+","+str(s_allstonks)+"  , in "+str(t2))
            if t2 > 180:
                print("unable to sleep")
                with open('logwriters.txt', 'a') as f2:
                    f2.write('\nUnable sleep : ' +datetime.now().strftime("%Y%d%m %H%M%S"))
            else:
                print('Waiting for'+str(180-t2))
                time.sleep(180-t2)        #df['time'] = dt_string
            current_time = datetime.datetime.now()        
           
        except Exception as e:
            print('error'+str(e))
    if not running_status():
        print('\nmarket Closed')
allStonks=fnolist()
s_allstonks=set(allStonks)-set(['NIFTY', 'FINNIFTY', 'BANKNIFTY','NIFTYIT'])
s_allstonks=sorted(list(s_allstonks))
#composite_list = [my_list[x:x+5] for x in range(0, len(my_list),5)]
l=[]
t=0
for i in range(0,len(s_allstonks),10):
    
    if(i+5<(len(s_allstonks)-1)):
        l.append(s_allstonks[i:i+10])
    else:
        l.append(s_allstonks[i:len(s_allstonks)%10])
l.append(s_allstonks[10*(len(l)-1):])   
#l2=l[0:5]
#for la in l2:
#    printAll(la)
import requests, zipfile, io
import concurrent.futures
now=datetime.now()
with concurrent.futures.ThreadPoolExecutor() as exector : 
   exector.map(printAll, l)

