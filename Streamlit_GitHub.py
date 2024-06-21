# 載入必要模組
import pandas as pd
import streamlit as st
import datetime
import numpy as np
import streamlit.components.v1 as stc 
import plotly.graph_objects as go
from plotly.subplots import make_subplots

###### (1) 開始設定 ######
html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">金融資料視覺化呈現 (金融看板) </h1>
		<h2 style="color:white;text-align:center;">Financial Dashboard </h2>
		</div>
		"""
stc.html(html_temp)

# 載入資料
@st.cache_data(ttl=3600, show_spinner="正在加載資料...") 
def load_data(url):
    df = pd.read_csv(url)
    return df

file_path = r'C:\Users\DING\Downloads\2303.csv'
df_original = load_data(file_path)

# 將日期轉換為datetime格式
df_original['Date'] = pd.to_datetime(df_original['Date'])

##### 選擇資料區間
st.subheader("選擇開始與結束的日期")
start_date = st.date_input('選擇開始日期', min_value=df_original['Date'].min(), max_value=df_original['Date'].max(), value=df_original['Date'].min())
end_date = st.date_input('選擇結束日期', min_value=df_original['Date'].min(), max_value=df_original['Date'].max(), value=df_original['Date'].max())

# 使用條件篩選選擇時間區間的數據
df = df_original[(df_original['Date'] >= start_date) & (df_original['Date'] <= end_date)]

######  (2) 轉化為字典 ######
KBar_dic = {
    'time': np.array(df['Date']),  # 使用日期作為時間
    'open': np.array(df['Open']),
    'high': np.array(df['High']),
    'low': np.array(df['Low']),
    'close': np.array(df['Close']),
    'volume': np.array(df['Volume']),
    'product': np.repeat('2303', len(df))  # 產品代碼，這裡假設是股票代號 2303
}

######  (3) 設置KBar物件及參數 ######
class KBar:
    def __init__(self, date_array, cycle_duration):
        self.TAKBar = {
            'time': date_array,
            'open': KBar_dic['open'],
            'high': KBar_dic['high'],
            'low': KBar_dic['low'],
            'close': KBar_dic['close'],
            'volume': KBar_dic['volume']
        }

Date = np.array(KBar_dic['time'])
cycle_duration = st.number_input('輸入一根 K 棒的時間長度(分鐘)', min_value=1, value=1440, step=1)
KBar = KBar(Date, cycle_duration)

###### (4) 繪製圖表 ######
st.subheader("畫圖")

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Candlestick(x=KBar.TAKBar['time'],
                open=KBar.TAKBar['open'], high=KBar.TAKBar['high'],
                low=KBar.TAKBar['low'], close=KBar.TAKBar['close'], name='K線'),
               secondary_y=True)

fig.add_trace(go.Bar(x=KBar.TAKBar['time'], y=KBar.TAKBar['volume'], name='成交量', marker=dict(color='black')), secondary_y=False)

fig.layout.yaxis2.showgrid=True
st.plotly_chart(fig, use_container_width=True)
