# 載入必要模組
import os
#os.chdir(r'C:\Users\user\Dropbox\系務\專題實作\112\金融看板\for students')
#import haohaninfo
#from order_Lo8 import Record
import numpy as np
#from talib.abstract import SMA,EMA, WMA, RSI, BBANDS, MACD
#import sys
import indicator_f_Lo2_short,datetime, indicator_forKBar_short
#import datetime
import pandas as pd
import streamlit as st 
import streamlit.components.v1 as stc 


###### (1) 開始設定 ######
html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">金融資料視覺化呈現 (金融看板) </h1>
		<h2 style="color:white;text-align:center;">Financial Dashboard </h2>
		</div>
		"""
stc.html(html_temp)


# 讀取CSV檔案並保存為PKL檔案
df = pd.read_csv("2303.TW.csv")
df.to_pickle('2303.TW.pkl')

# 定義用於從PKL檔案中讀取資料的函式
@st.cache(ttl=3600, show_spinner="正在加載資料...") 
def load_data(url):
    df = pd.read_pickle(url)
    return df


#df_original = load_data('2303.TW.pkl')

#df.columns  ## Index(['Unnamed: 0', 'time', 'open', 'low', 'high', 'close', 'volume','amount'], dtype='object')
##df = df.drop('Unnamed: 0',axis=1)
#df.columns  ## Index(['time', 'open', 'low', 'high', 'close', 'volume', 'amount'], dtype='object')
#df['time']
#type(df['time'])  ## pandas.core.series.Series
#df['time'][11]
#df.head()
#df.tail()
#type(df['time'][0])


##### 選擇資料區間
st.subheader("選擇開始與結束的日期, 區間:2020/01/01 至 2024/06/20")
start_date = st.text_input('選擇開始日期 (日期格式: 2020/01/01)', '2020/01/01')
end_date = st.text_input('選擇結束日期 (日期格式: 2024/06/20)', '2024/06/20')

# 將日期字符串轉換為 datetime 對象
start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d')
end_date = datetime.datetime.strptime(end_date, '%Y/%m/%d')

# 使用條件篩選選擇時間區間的資料
df['Date'] = pd.to_datetime(df['Date'])  # 將日期欄位轉換為 datetime 對象（如果尚未轉換）
df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]


###### (2) 轉化為字典 ######:
KBar_dic = df.to_dict()
#type(KBar_dic)
#KBar_dic.keys()  ## dict_keys(['time', 'open', 'low', 'high', 'close', 'volume', 'amount'])
#KBar_dic['open']
#type(KBar_dic['open'])  ## dict
#KBar_dic['open'].values()
#type(KBar_dic['open'].values())  ## dict_values
KBar_Open_list = list(KBar_dic['Open'].values())
KBar_dic['Open']=np.array(KBar_Open_list)
#type(KBar_dic['open'])  ## numpy.ndarray
#KBar_dic['open'].shape  ## (1596,)
#KBar_dic['open'].size   ##  1596

KBar_dic['Product'] = np.repeat('UMC', KBar_dic['Open'].size)
#KBar_dic['product'].size   ## 1596
#KBar_dic['product'][0]      ## 'tsmc'

KBar_Date_list = list(KBar_dic['Date'].values())
KBar_Date_list = [i.to_pydatetime() for i in KBar_Date_list] ## Timestamp to datetime
KBar_dic['Date']=np.array(KBar_Date_list)

# KBar_time_list[0]        ## Timestamp('2022-07-01 09:01:00')
# type(KBar_time_list[0])  ## pandas._libs.tslibs.timestamps.Timestamp
#KBar_time_list[0].to_pydatetime() ## datetime.datetime(2022, 7, 1, 9, 1)
#KBar_time_list[0].to_numpy()      ## numpy.datetime64('2022-07-01T09:01:00.000000000')
#KBar_dic['time']=np.array(KBar_time_list)
#KBar_dic['time'][80]   ## Timestamp('2022-09-01 23:02:00')

KBar_Low_list = list(KBar_dic['Low'].values())
KBar_dic['Low']=np.array(KBar_Low_list)

KBar_High_list = list(KBar_dic['High'].values())
KBar_dic['High']=np.array(KBar_High_list)

KBar_Close_list = list(KBar_dic['Close'].values())
KBar_dic['Close']=np.array(KBar_Close_list)

KBar_Volume_list = list(KBar_dic['Volume'].values())
KBar_dic['Volume']=np.array(KBar_Volume_list)

#KBar_Adj_Close_array = KBar_dic['Adj Close'].values
#KBar_dic['Adj Close'] = KBar_Adj_Close_array

#KBar_amount_list = list(KBar_dic['amount'].values())
#KBar_dic['amount']=np.array(KBar_amount_list)


######  (3) 改變 KBar 時間長度 (以下)  ########
# Product_array = np.array([])
# Time_array = np.array([])
# Open_array = np.array([])
# High_array = np.array([])
# Low_array = np.array([])
# Close_array = np.array([])
# Volume_array = np.array([])

Date = start_date.strftime("%Y-%m-%d")

st.subheader("設定一根 K 棒的時間長度(分鐘)")
cycle_duration = st.number_input('輸入一根 K 棒的時間長度(單位:分鐘, 一日=1440分鐘)', value=(1440), key="KBar_duration")
cycle_duration = int(cycle_duration)
#cycle_duration = 1440   ## 可以改成你想要的 KBar 週期
#KBar = indicator_f_Lo2.KBar(Date,'time',2)
KBar = indicator_forKBar_short.KBar(Date,cycle_duration)    ## 設定cycle_duration可以改成你想要的 KBar 週期

#KBar_dic['amount'].shape   ##(5585,)
#KBar_dic['amount'].size    ##5585
#KBar_dic['time'].size    ##5585

for i in range(KBar_dic['Date'].size):
    
    #time = datetime.datetime.strptime(KBar_dic['time'][i],'%Y%m%d%H%M%S%f')
    Date = KBar_dic['Date'][i]
    #prod = KBar_dic['product'][i]
    Open_price= KBar_dic['Open'][i]
    Close_price= KBar_dic['Close'][i]
    Low_price= KBar_dic['Low'][i]
    High_price= KBar_dic['High'][i]
    Volume =  KBar_dic['Volume'][i]
    #Adj_close = KBar_dic['Adj Close'][i]
    #tag=KBar.TimeAdd(time,price,qty,prod)
    tag=KBar.AddPrice(Date, Open_price, Close_price, Low_price, High_price, Volume)
    
    # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行, 因為計算 MA是利用收盤價, 而在 KBar class 中的 "TimeAdd"函數方法中, 收盤價只是一直附加最新的 price 而已.
    #if tag != 1:
        #continue
    #print(KBar.Time,KBar.GetOpen(),KBar.GetHigh(),KBar.GetLow(),KBar.GetClose(),KBar.GetVolume()) 
    
    
        
# #type(KBar.Time[1:-1]) ##numpy.ndarray       
# Time_array =  np.append(Time_array, KBar.Time[1:-1])    
# Open_array =  np.append(Open_array,KBar.Open[1:-1])
# High_array =  np.append(High_array,KBar.High[1:-1])
# Low_array =  np.append(Low_array,KBar.Low[1:-1])
# Close_array =  np.append(Close_array,KBar.Close[1:-1])
# Volume_array =  np.append(Volume_array,KBar.Volume[1:-1])
# Product_array = np.append(Product_array,KBar.Prod[1:-1])

KBar_dic = {}

# ## 形成 KBar 字典:
# KBar_dic['time'] =  Time_array   
# KBar_dic['product'] =  Product_array
# KBar_dic['open'] =  Open_array
# KBar_dic['high'] =  High_array
# KBar_dic['low'] =  Low_array
# KBar_dic['close'] =  Close_array
# KBar_dic['volume'] =  Volume_array

 ## 形成 KBar 字典 (新週期的):
KBar_dic['Date'] =  KBar.TAKBar['Date']   
#KBar_dic['product'] =  KBar.TAKBar['product']
KBar_dic['Product'] = np.repeat('UMC', KBar_dic['Date'].size)
KBar_dic['Open'] = KBar.TAKBar['Open']
KBar_dic['High'] =  KBar.TAKBar['High']
KBar_dic['Low'] =  KBar.TAKBar['Low']
KBar_dic['Close'] =  KBar.TAKBar['Close']
KBar_dic['Volume'] =  KBar.TAKBar['Volume']
# KBar_dic['time'].shape  ## (2814,)
# KBar_dic['open'].shape  ## (2814,)
# KBar_dic['high'].shape  ## (2814,)
# KBar_dic['low'].shape  ## (2814,)
# KBar_dic['close'].shape  ## (2814,)
# KBar_dic['volume'].shape  ## (2814,)
#KBar_dic['time'][536]
######  改變 KBar 時間長度 (以上)  ########



###### (4) 計算各種技術指標 ######
##### 將K線 Dictionary 轉換成 Dataframe
KBar_df = pd.DataFrame(KBar_dic)


#####  (i) 移動平均線策略   #####
####  設定長短移動平均線的 K棒 長度:
st.subheader("設定計算長移動平均線(MA)的 K 棒數目(整數, 例如 10)")
#LongMAPeriod=st.number_input('輸入一個整數', key="Long_MA")
#LongMAPeriod=int(LongMAPeriod)
LongMAPeriod=st.slider('選擇一個整數', 0, 100, 10)
st.subheader("設定計算短移動平均線(MA)的 K 棒數目(整數, 例如 2)")
#ShortMAPeriod=st.number_input('輸入一個整數', key="Short_MA")
#ShortMAPeriod=int(ShortMAPeriod)
ShortMAPeriod=st.slider('選擇一個整數', 0, 100, 2)

#### 計算長短移動平均線
KBar_df['MA_long'] = KBar_df['Close'].rolling(window=LongMAPeriod).mean()
KBar_df['MA_short'] = KBar_df['Close'].rolling(window=ShortMAPeriod).mean()

#### 尋找最後 NAN值的位置
last_nan_index_MA = KBar_df['MA_long'][::-1].index[KBar_df['MA_long'][::-1].apply(pd.isna)][0]



#####  (ii) RSI 策略   #####
#### 順勢策略
### 設定長短 RSI 的 K棒 長度:
st.subheader("設定計算長RSI的 K 棒數目(整數, 例如 10)")
LongRSIPeriod=st.slider('選擇一個整數', 0, 1000, 10)
st.subheader("設定計算短RSI的 K 棒數目(整數, 例如 2)")
ShortRSIPeriod=st.slider('選擇一個整數', 0, 1000, 2)

### 計算 RSI指標長短線, 以及定義中線
## 假设 df 是一个包含价格数据的Pandas DataFrame，其中 'close' 是KBar週期收盤價
def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

KBar_df['RSI_long'] = calculate_rsi(KBar_df, LongRSIPeriod)
KBar_df['RSI_short'] = calculate_rsi(KBar_df, ShortRSIPeriod)
KBar_df['RSI_Middle']=np.array([50]*len(KBar_dic['Date']))

### 尋找最後 NAN值的位置
last_nan_index_RSI = KBar_df['RSI_long'][::-1].index[KBar_df['RSI_long'][::-1].apply(pd.isna)][0]


# #### 逆勢策略
# ### 建立部位管理物件
# OrderRecord=Record() 
# ### 計算 RSI指標, 天花板與地板
# RSIPeriod=5
# Ceil=80
# Floor=20
# MoveStopLoss=30
# KBar_dic['RSI']=RSI(KBar_dic,timeperiod=RSIPeriod)
# KBar_dic['Ceil']=np.array([Ceil]*len(KBar_dic['time']))
# KBar_dic['Floor']=np.array([Floor]*len(KBar_dic['time']))

# ### 將K線 Dictionary 轉換成 Dataframe
# KBar_RSI_df=pd.DataFrame(KBar_dic)


###### (5) 將 Dataframe 欄位名稱轉換  ###### 
KBar_df.columns = [ i[0].upper()+i[1:] for i in KBar_df.columns ]


###### (6) 畫圖 ######
st.subheader("畫圖")
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
#from plotly.offline import plot
import plotly.offline as pyoff


##### K線圖, 移動平均線 MA
with st.expander("K線圖, 移動平均線"):
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    
    #### include candlestick with rangeselector
    fig1.add_trace(go.Candlestick(x=KBar_df['Date'],
                    open=KBar_df['Open'], high=KBar_df['High'],
                    low=KBar_df['Low'], close=KBar_df['Close'], name='K線'),
                   secondary_y=True)   ## secondary_y=True 表示此圖形的y軸scale是在右邊而不是在左邊
    
    #### include a go.Bar trace for volumes
    fig1.add_trace(go.Bar(x=KBar_df['Date'], y=KBar_df['Volume'], name='成交量', marker=dict(color='black')),secondary_y=False)  ## secondary_y=False 表示此圖形的y軸scale是在左邊而不是在右邊
    fig1.add_trace(go.Scatter(x=KBar_df['Date'][last_nan_index_MA+1:], y=KBar_df['MA_long'][last_nan_index_MA+1:], mode='lines',line=dict(color='orange', width=2), name=f'{LongMAPeriod}-根 K棒 移動平均線'), 
                  secondary_y=True)
    fig1.add_trace(go.Scatter(x=KBar_df['Date'][last_nan_index_MA+1:], y=KBar_df['MA_short'][last_nan_index_MA+1:], mode='lines',line=dict(color='pink', width=2), name=f'{ShortMAPeriod}-根 K棒 移動平均線'), 
                  secondary_y=True)
    
    fig1.layout.yaxis2.showgrid=True
    st.plotly_chart(fig1, use_container_width=True)


##### K線圖, RSI
with st.expander("K線圖, 長短 RSI"):
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    #### include candlestick with rangeselector
    fig2.add_trace(go.Candlestick(x=KBar_df['Date'],
                    open=KBar_df['Open'], high=KBar_df['High'],
                    low=KBar_df['Low'], close=KBar_df['Close'], name='K線'),
                   secondary_y=True)   ## secondary_y=True 表示此圖形的y軸scale是在右邊而不是在左邊
    
    fig2.add_trace(go.Scatter(x=KBar_df['Date'][last_nan_index_RSI+1:], y=KBar_df['RSI_long'][last_nan_index_RSI+1:], mode='lines',line=dict(color='red', width=2), name=f'{LongRSIPeriod}-根 K棒 移動 RSI'), 
                  secondary_y=False)
    fig2.add_trace(go.Scatter(x=KBar_df['Date'][last_nan_index_RSI+1:], y=KBar_df['RSI_short'][last_nan_index_RSI+1:], mode='lines',line=dict(color='blue', width=2), name=f'{ShortRSIPeriod}-根 K棒 移動 RSI'), 
                  secondary_y=False)
    
    fig2.layout.yaxis2.showgrid=True
    st.plotly_chart(fig2, use_container_width=True)













