import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox
from matplotlib import style
import sys
import random
import argparse
from nsepython import *
import datetime
##style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(2,1,2)
ax2 = fig.add_subplot(2,1,1)
data1 = np.zeros(1)
fnos=fnolist()
plt.subplots_adjust(bottom=0.2)
import matplotlib.pyplot as plt
def getOI(symbol):
    lot_size=nse_get_fno_lot_sizes(symbol)
    optionchain=(nse_optionchain_scrapper(symbol))
    optionchain_Json= (optionchain)
    data_only=json.dumps(optionchain_Json['records']['data'])
    dict_only=optionchain_Json['records']['data']
    expiries=optionchain['records']['expiryDates']
    df=pd.json_normalize(dict_only)
    df=df[[ "PE.strikePrice", "PE.expiryDate", "PE.underlying", "PE.identifier", "PE.openInterest", "PE.changeinOpenInterest", "PE.pchangeinOpenInterest", "PE.totalTradedVolume", "PE.impliedVolatility", "PE.lastPrice", "PE.change", "PE.pChange", "PE.totalBuyQuantity", "PE.totalSellQuantity", "PE.bidQty", "PE.bidprice", "PE.askQty", "PE.askPrice", "PE.underlyingValue", "strikePrice", "expiryDate", "CE.strikePrice", "CE.expiryDate", "CE.underlying", "CE.identifier", "CE.openInterest", "CE.changeinOpenInterest", "CE.pchangeinOpenInterest", "CE.totalTradedVolume", "CE.impliedVolatility", "CE.lastPrice", "CE.change", "CE.pChange", "CE.totalBuyQuantity", "CE.totalSellQuantity", "CE.bidQty", "CE.bidprice", "CE.askQty", "CE.askPrice", "CE.underlyingValue"]]
    df2=df.drop(["PE.underlying", "PE.identifier",  "PE.totalTradedVolume", "PE.change", "PE.pChange", "PE.totalBuyQuantity", "PE.totalSellQuantity", "PE.bidQty", "PE.bidprice", "PE.askQty", "PE.askPrice", "PE.underlyingValue", "strikePrice", "expiryDate", "CE.strikePrice", "CE.expiryDate", "CE.underlying", "CE.identifier","CE.totalTradedVolume","CE.change", "CE.pChange", "CE.totalBuyQuantity", "CE.totalSellQuantity", "CE.bidQty", "CE.bidprice", "CE.askQty", "CE.askPrice", "CE.underlyingValue"], axis=1)
    df=df.drop(["PE.underlying", "CE.underlying","PE.strikePrice", "PE.change", "PE.pChange", "CE.change", "CE.pChange","CE.strikePrice", "CE.expiryDate","PE.expiryDate", "PE.underlying", "PE.identifier", "CE.identifier","PE.changeinOpenInterest", "PE.pchangeinOpenInterest","CE.changeinOpenInterest", "CE.pchangeinOpenInterest", "PE.bidQty", "PE.bidprice", "PE.askQty", "PE.askPrice", "CE.bidQty", "CE.bidprice", "CE.askQty", "CE.askPrice"], axis=1)
    df2['CE.openInterest'] = df2['CE.openInterest'].apply(lambda x: x*lot_size/100000)
    df2['PE.openInterest'] = df2['PE.openInterest'].apply(lambda x: x*lot_size/100000)
    df2['CE.changeinOpenInterest'] = df2['CE.changeinOpenInterest'].apply(lambda x: x*lot_size/100000)
    df2['PE.changeinOpenInterest'] = df2['PE.changeinOpenInterest'].apply(lambda x: x*lot_size/100000)
    ltp = float(optionchain['records']['underlyingValue'])
    strike_price_list = [x['strikePrice'] for x in optionchain['records']['data']]
    atm_strike = sorted([[round(abs(ltp-i),2),i] for i in strike_price_list])[0][1]
    return df2,atm_strike
def animate(i):
    
    symbol=textbox.text.upper()
    if(symbol not in fnos):
        ax1.set_title('NOt Valid FNO STOCK name')
        symbol='SBIN'
    data,atm=getOI(symbol)
    data=data.dropna()
    expirs=data['PE.expiryDate'].unique()
    
    data=data[data['PE.expiryDate'].str.contains(expirs[0])]
    
    strikes=list(data['PE.strikePrice'].unique())
    strikeDiffs=float(strikes[2])-float(strikes[1])
       

    numStrike=10
    try:
        numStrike=int(float(textbox2.text))
    except:
        numStrike=10
    data=data[(data['PE.strikePrice']>(atm-strikeDiffs*numStrike))&(data['PE.strikePrice']<(atm+strikeDiffs*numStrike))]
    bar_width =strikeDiffs*0.1
    
    indices = list(data['PE.strikePrice'])
    index_=indices.index(atm)
    fig = plt.figure()
    
    #y1 = data[indices,index_].astype(float)
    #y2 = data[indices,-1-index_].astype(float)
    ax1.cla()
    ax2.cla()
    indices_offset=[x+bar_width for x in indices]
    ax1.bar(indices,data['PE.openInterest'],bar_width,color='g',label = 'Puts')
    ax1.bar(indices_offset,data['CE.openInterest'],bar_width,color='r',label = 'Calls')
    ax2.bar(indices,data['PE.changeinOpenInterest'],bar_width,color='g',label = 'Puts Change')
    ax2.bar(indices_offset,data['CE.changeinOpenInterest'],bar_width,color='r',label = 'Calls Change')
    ax1.set_xlabel('Strike Prices')
    ax1.set_ylabel('OI lakhs')
    ax2.set_ylabel('OI Change lakhs')
    ax2.set_title(symbol+' , ATM : '+ str(atm)+' at      '+datetime.datetime.now().strftime("%d %B %H:%M:%S"))
    ax2.set_xticks([x+bar_width/2 for x in indices])
    
    ax1.set_xticks([x+bar_width/2 for x in indices])
    ax1.set_xticklabels(indices,rotation=90)
    ax2.set_xticklabels(indices,rotation=90)
    ax1.legend()
    ax2.legend()
    ax1.grid()
    ax2.grid()
    plt.close(fig)
ani = animation.FuncAnimation(fig,animate,interval=2000)
ax_box=plt.axes([0.3,0.08,0.1,0.05])
ax_box2=plt.axes([0.6,0.08,0.1,0.05])
textbox=TextBox(ax_box,'Symbol',initial='SBIN')
textbox2=TextBox(ax_box2,'No of Strikes:',initial='10')

plt.show()
