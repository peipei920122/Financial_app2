# 載入必要模組
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 讀取CSV檔案並保存為PKL檔案（如果已經有PKL檔案，則可以跳過這步）
df = pd.read_csv("2303.TW.csv")
df.to_pickle('2303.TW.pkl')

# 定義用於從PKL檔案中讀取資料的函式（使用streamlit的cache功能來加速資料讀取）
@st.cache(ttl=3600, show_spinner="正在加載資料...") 
def load_data(url):
    df = pd.read_pickle(url)
    return df

# 加載數據
df = load_data('2303.TW.pkl')

# 選擇資料區間
st.subheader("選擇開始與結束的日期, 區間:2020/01/01 至 2024/06/20")
start_date = st.text_input('選擇開始日期 (日期格式: 2020/01/01)', '2020/01/01')
end_date = st.text_input('選擇結束日期 (日期格式: 2024/06/20)', '2024/06/20')

# 將日期字符串轉換為 datetime 對象
start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d')
end_date = datetime.datetime.strptime(end_date, '%Y/%m/%d')

# 使用條件篩選選擇時間區間的資料
df['Date'] = pd.to_datetime(df['Date'])  # 將日期欄位轉換為 datetime 對象（如果尚未轉換）
df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# 設定 KBar 的時間長度
st.subheader("設定一根 K 棒的時間長度(分鐘)")
cycle_duration = st.number_input('輸入一根 K 棒的時間長度(單位:分鐘, 一日=1440分鐘)', value=1440, key="KBar_duration")
KBar = indicator_forKBar_short.KBar(start_date.strftime("%Y-%m-%d"), cycle_duration)  # 初始化 KBar 物件

# 將數據加入 KBar
for i in range(df_filtered.shape[0]):
    Date = df_filtered.iloc[i]['Date']
    Open_price = df_filtered.iloc[i]['Open']
    Close_price = df_filtered.iloc[i]['Close']
    Low_price = df_filtered.iloc[i]['Low']
    High_price = df_filtered.iloc[i]['High']
    Volume = df_filtered.iloc[i]['Volume']
    KBar.AddPrice(Date, Open_price, Close_price, Low_price, High_price, Volume)

# 轉換 KBar 為字典
KBar_dic = {
    'Date': KBar.TAKBar['Date'],
    'Product': np.repeat('UMC', KBar.TAKBar['Date'].size),
    'Open': KBar.TAKBar['Open'],
    'High': KBar.TAKBar['High'],
    'Low': KBar.TAKBar['Low'],
    'Close': KBar.TAKBar['Close'],
    'Volume': KBar.TAKBar['Volume']
}

# 計算移動平均線
st.subheader("計算移動平均線")
LongMAPeriod = st.slider('選擇長期移動平均線的 K 棒數目', 0, 100, 10)
ShortMAPeriod = st.slider('選擇短期移動平均線的 K 棒數目', 0, 100, 2)

KBar_df = pd.DataFrame(KBar_dic)
KBar_df['MA_long'] = KBar_df['Close'].rolling(window=LongMAPeriod).mean()
KBar_df['MA_short'] = KBar_df['Close'].rolling(window=ShortMAPeriod).mean()

# 繪製移動平均線圖
st.subheader("畫圖 - 移動平均線")
fig_ma = make_subplots(specs=[[{"secondary_y": True}]])
fig_ma.add_trace(go.Candlestick(x=KBar_df['Date'], open=KBar_df['Open'], high=KBar_df['High'],
                                low=KBar_df['Low'], close=KBar_df['Close'], name='K線'), secondary_y=True)
fig_ma.add_trace(go.Scatter(x=KBar_df['Date'], y=KBar_df['MA_long'], mode='lines', name=f'{LongMAPeriod}-根 K 棒移動平均線', line=dict(color='orange', width=2)), secondary_y=True)
fig_ma.add_trace(go.Scatter(x=KBar_df['Date'], y=KBar_df['MA_short'], mode='lines', name=f'{ShortMAPeriod}-根 K 棒移動平均線', line=dict(color='pink', width=2)), secondary_y=True)
fig_ma.layout.yaxis2.showgrid=True
st.plotly_chart(fig_ma, use_container_width=True)

# 計算 RSI 指標
st.subheader("計算 RSI 指標")
LongRSIPeriod = st.slider('選擇長期 RSI 的 K 棒數目', 0, 1000, 10)
ShortRSIPeriod = st.slider('選擇短期 RSI 的 K 棒數目', 0, 1000, 2)

def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

KBar_df['RSI_long'] = calculate_rsi(KBar_df, LongRSIPeriod)
KBar_df['RSI_short'] = calculate_rsi(KBar_df, ShortRSIPeriod)
KBar_df['RSI_Middle'] = np.array([50] * len(KBar_dic['Date']))

# 繪製 RSI 圖
st.subheader("畫圖 - RSI 指標")
fig_rsi = make_subplots(specs=[[{"secondary_y": True}]])
fig_rsi.add_trace(go.Candlestick(x=KBar_df['Date'], open=KBar_df['Open'], high=KBar_df['High'],
                                 low=KBar_df['Low'], close=KBar_df['Close'], name='K線'), secondary_y=True)
fig_rsi.add_trace(go.Scatter(x=KBar_df['Date'], y=KBar_df['RSI_long'], mode='lines', name=f'{LongRSIPeriod}-根 K 棒 RSI', line=dict(color='red', width=2)), secondary_y=False)
fig_rsi.add_trace(go.Scatter(x=KBar_df['Date'], y=KBar_df['RSI_short'], mode='lines', name=f'{ShortRSIPeriod}-根 K 棒 RSI', line=dict(color='blue', width=2)), secondary_y=False)
fig_rsi.layout.yaxis2.showgrid=True
st.plotly_chart(fig_rsi, use_container_width=True)
