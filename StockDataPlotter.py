import os
import glob
from math import nan
import pandas as pd
from PyQt5.QtWidgets import QComboBox, QCheckBox, QWidget
from pyqtgraph import QtGui
import pyqtgraph as pg
import requests
import finplot as fplt


def returnStrikeOHLC(cOrP,sym, strike,expiry):
    df=pd.read_csv(sym+"_chain.csv")
    df_thisStrike=df[(df.OPTION_TYP.eq(cOrP)) & (df.STRIKE_PR.eq(strike))&(df.EXPIRY_DT.eq(expiry))]
    df_thisStrike=df_thisStrike.drop(["SYMBOL","EXPIRY_DT","STRIKE_PR","OPTION_TYP","CONTRACTS","VAL_INLAKH","OPEN_INT","CHG_IN_OI"], axis=1)
    df_thisStrike = df_thisStrike[['TIMESTAMP','OPEN','HIGH','LOW','CLOSE']]
    df_thisStrike =df_thisStrike[df_thisStrike['OPEN']!=0]
    return df_thisStrike
def getExpiries(sym):
    df=pd.read_csv(sym+"_chain.csv")
    allexp=df.EXPIRY_DT.unique()
    print(allexp)
    return allexp
def getStrikes(sym,exps):
    df=pd.read_csv(sym+"_chain.csv")
    allexp=df[df['EXPIRY_DT']==exps]['STRIKE_PR'].unique()
    return sorted(allexp)
def returnStock(sym,interval):
    df=pd.read_csv(sym+"_"+interval+".csv",parse_dates=True,index_col=0)
	# df.columns = ['','Open','High','Low','Close']
    #df.rename( columns={0 :'Datetime'}, inplace=True )
    return df
def create_ctrl_panel(win):
   
    panel = QWidget(win)
    panel.move(100, 0)
    win.scene().addWidget(panel)
    layout = QtGui.QGridLayout(panel)
    
    panel.symbol = QComboBox(panel)
    [panel.symbol.addItem(i) for i in 'AARTIIND ABBOTINDIA ABFRL ACC ADANIENT ADANIPORTS ADANIPOWER AJANTPHARM ALBK ALKEM AMARAJABAT AMBUJACEM ANDHRABANK APLLTD APOLLOHOSP APOLLOTYRE ARVIND ASHOKLEY ASIANPAINT ASTRAL ATUL AUBANK AUROPHARMA AXISBANK BAJAJ-AUTO BAJAJFINSV BAJFINANCE BALKRISIND BALRAMCHIN BANDHANBNK BANKBARODA BANKINDIA BATAINDIA BEL BEML BERGEPAINT BHARATFIN BHARATFORG BHARTIARTL BHEL BIOCON BOSCHLTD BPCL BRITANNIA BSOFT CADILAHC CANBK CANFINHOME CAPF CASTROLIND CEATLTD CENTURYTEX CESC CGPOWER CHAMBLFERT CHENNPETRO CHOLAFIN CIPLA COALINDIA COFORGE COLPAL CONCOR COROMANDEL CROMPTON CUB CUMMINSIND DABUR DALBHARAT DALMIABHA DCBBANK DEEPAKNTR DELTACORP DHFL DISHTV DIVISLAB DIXON DLF DRREDDY EICHERMOT ENGINERSIN EQUITAS ESCORTS EXIDEIND FEDERALBNK FORTIS FSL GAIL GLENMARK GMRINFRA GODFRYPHLP GODREJCP GODREJIND GODREJPROP GRANULES GRASIM GSFC GSPL GUJGASLTD HAL HAVELLS HCC HCLTECH HDFC HDFCAMC HDFCBANK HDFCLIFE HDIL HEROMOTOCO HEXAWARE HINDALCO HINDPETRO HINDUNILVR HINDZINC IBULHSGFIN ICICIBANK ICICIGI ICICIPRULI ICIL IDBI IDEA IDFC IDFCBANK IDFCFIRSTB IEX IFCI IGL INDHOTEL INDIACEM INDIAMART INDIANB INDIGO INDUSINDBK INDUSTOWER INFIBEAM INFRATEL INFY IOC IPCALAB IRB IRCTC ITC JETAIRWAYS JINDALSTEL JISLJALEQS JKCEMENT JPASSOCIAT JSWENERGY JSWSTEEL JUBLFOOD JUSTDIAL KAJARIACER KOTAKBANK KPIT KSCL KTKBANK L&TFH LALPATHLAB LAURUSLABS LICHSGFIN LT LTI LTTS LUPIN M&M M&MFIN MANAPPURAM MARICO MARUTI MCDOWELL-N MCX METROPOLIS MFSL MGL MINDTREE MOTHERSUMI MPHASIS MRF MRPL MUTHOOTFIN NAM-INDIA NATIONALUM NAUKRI NAVINFLUOR NBCC NCC NESTLEIND NHPC NIITTECH NMDC NTPC OBEROIRLTY OFSS OIL ONGC ORIENTBANK PAGEIND PCJEWELLER PEL PERSISTENT PETRONET PFC PFIZER PIDILITIND PIIND PNB POLYCAB POWERGRID PTC PVR RAMCOCEM RAYMOND RBLBANK RCOM RECLTD RELCAPITAL RELIANCE RELINFRA REPCOHOME RNAVAL RPOWER SAIL SBICARD SBILIFE SBIN SHREECEM SIEMENS SOUTHBANK SREINFRA SRF SRTRANSFIN STAR SUNPHARMA SUNTV SUZLON SYNDIBANK SYNGENE TATACHEM TATACOMM TATACONSUM TATAELXSI TATAGLOBAL TATAMOTORS TATAMTRDVR TATAPOWER TATASTEEL TCS TECHM TITAN TORNTPHARM TORNTPOWER TRENT TV18BRDCST TVSMOTOR UBL UJJIVAN ULTRACEMCO UNIONBANK UPL VEDL VGUARD VOLTAS WHIRLPOOL WIPRO WOCKPHARMA YESBANK ZEEL '.split()]
    panel.symbol.resize(165,60)
    panel.symbol.setCurrentIndex(1)
    layout.addWidget(panel.symbol, 0, 0)
    panel.symbol.currentTextChanged.connect(change_asset)
    
    panel.optOrStock = QComboBox(panel)
    [panel.optOrStock.addItem(i) for i in 'Stock Options'.split()]
    panel.optOrStock.resize(165,60)
    panel.optOrStock.setCurrentIndex(0)
    layout.addWidget(panel.optOrStock, 0, 1)
    #panel.optOrStock.currentTextChanged.connect(change_asset)

    layout.setColumnMinimumWidth(1, 30)
    panel.interval = QComboBox(panel)
    [panel.interval.addItem(i) for i in '1MO:1d:30m:15m'.split(":")]
    panel.interval.setCurrentIndex(1)
    layout.addWidget(panel.interval, 0, 2)
    panel.interval.currentTextChanged.connect(change_asset)
    panel.indicators = QComboBox(panel)
    [panel.indicators.addItem(i) for i in 'Clean:Few indicators'.split(':')]
    panel.indicators.setCurrentIndex(1)
    layout.addWidget(panel.indicators, 0, 4)
    panel.indicators.currentTextChanged.connect(change_asset)

    layout.setColumnMinimumWidth(5, 30)

    return panel
def calc_rsi(price, n=14, ax=None):
    diff = price.diff().values
    gains = diff
    losses = -diff
    gains[~(gains>0)] = 0.0
    losses[~(losses>0)] = 1e-10 # we don't want divide by zero/NaN
    m = (n-1) / n
    ni = 1 / n
    g = gains[n] = gains[:n].mean()
    l = losses[n] = losses[:n].mean()
    gains[:n] = losses[:n] = nan
    for i,v in enumerate(gains[n:],n):
        g = gains[i] = ni*v + m*g
    for i,v in enumerate(losses[n:],n):
        l = losses[i] = ni*v + m*l
    rs = gains / losses
    rsi = 100 - (100/(1+rs))
    return rsi

def calc_plot_data(df, indicators):
    '''Returns data for all plots and for the price line.'''
    price = df['Open Close High Low'.split()]
    volume = df['Open Close Volume'.split()]
    ma50 = ma200 = vema24 = sar = rsi = stoch = stoch_s = None
    if 'few' in indicators or 'moar' in indicators:
        ma50  = price.Close.rolling(50).mean()
        ma200 = price.Close.rolling(200).mean()
        vema24 = volume.Volume.ewm(span=24).mean()
    plot_data = dict(price=price, volume=volume, ma50=ma50, ma200=ma200, vema24=vema24, sar=sar, rsi=rsi, \
                     stoch=stoch, stoch_s=stoch_s)
    # for price line
    last_close = price.iloc[-1].Close
    last_col = fplt.candle_bull_color if last_close > price.iloc[-2].Close else fplt.candle_bear_color
    price_data = dict(last_close=last_close, last_col=last_col)
    return plot_data, price_data

def change_asset(*args, **kwargs):
    '''Resets and recalculates everything, and plots for the first time.'''
    # save window zoom position before resetting
    fplt._savewindata(fplt.windows[0])

    symbol = ctrl_panel.symbol.currentText()
    interval =  ctrl_panel.interval.currentText()
    #ws.close()
   # ws.df = None
    df = returnStock(symbol, interval=interval)
    #ws.reconnect(symbol, interval, df)

    # remove any previous plots
    ax.reset()
    axo.reset()
    ax_rsi.reset()

    # calculate plot data
    indicators = ctrl_panel.indicators.currentText().lower()
    data,price_data = calc_plot_data(df, indicators)

    # some space for legend
    ctrl_panel.move(100 if 'clean' in indicators else 200, 0)

    # plot data
    global plots
    plots = {}
    plots['price'] = fplt.candlestick_ochl(data['price'], ax=ax)
    plots['volume'] = fplt.volume_ocv(data['volume'], ax=axo)
    if data['ma50'] is not None:
        plots['ma50'] = fplt.plot(data['ma50'], legend='MA-50', ax=ax)
        plots['ma200'] = fplt.plot(data['ma200'], legend='MA-200', ax=ax)
        plots['vema24'] = fplt.plot(data['vema24'], color=4, legend='V-EMA-24', ax=axo)
    if data['rsi'] is not None:
        ax.set_visible(xaxis=False)
        ax_rsi.show()
        fplt.set_y_range(0, 100, ax=ax_rsi)
        fplt.add_band(30, 70, color='#6335', ax=ax_rsi)
        plots['sar'] = fplt.plot(data['sar'], color='#55a', style='+', width=0.6, legend='SAR', ax=ax)
        plots['rsi'] = fplt.plot(data['rsi'], legend='RSI', ax=ax_rsi)
        plots['stoch'] = fplt.plot(data['stoch'], color='#880', legend='Stoch', ax=ax_rsi)
        plots['stoch_s'] = fplt.plot(data['stoch_s'], color='#650', ax=ax_rsi)
    else:
        ax.set_visible(xaxis=True)
        ax_rsi.hide()

    # price line
    ax.price_line = pg.InfiniteLine(angle=0, movable=False, pen=fplt._makepen(fplt.candle_bull_body_color, style='.'))
    ax.price_line.setPos(price_data['last_close'])
    ax.price_line.pen.setColor(pg.mkColor(price_data['last_col']))
    ax.addItem(ax.price_line, ignoreBounds=True)

    # restores saved zoom position, if in range
    fplt.refresh()
plots = {}
fplt.y_pad = 0.07 # pad some extra (for control panel)
fplt.max_zoom_points = 7
fplt.autoviewrestore()
ax,ax_rsi,ax_macd = fplt.create_plot('test', rows=3, init_zoom_periods=300)
axo = ax.overlay()


ax_rsi.vb.setBackgroundColor(None) # don't use odd background color
ax.set_visible(xaxis=True)

ctrl_panel = create_ctrl_panel(ax.vb.win)
#dark_mode_toggle(True)
#change_asset()
change_asset()
fplt.show()
